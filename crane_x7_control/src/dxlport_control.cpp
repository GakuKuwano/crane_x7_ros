#include    <ros/ros.h>
#include    <ros/package.h>
#include    <angles/angles.h>
#include    <crane_x7_control/dxlport_control.h>
#include    <math.h>
#include    <stdio.h>

/* MACRO */
#define     DXLPOS2RAD(pos)    (( (pos*(360.0/POSITION_STEP) )/360) *2*M_PI)
#define     RAD2DXLPOS(rad)    (( ((rad)/2.0/M_PI)*360.0 ) * (POSITION_STEP / 360.0))


DXLPORT_CONTROL::DXLPORT_CONTROL( ros::NodeHandle handle, CONTROL_SETTING &setting )
{
    int j;
    int dxl_comm_result = COMM_TX_FAIL;             // Communication result
    uint8_t dxl_error = 0;                          // Dynamixel error

    init_stat = false;
    tx_err = rx_err = 0;
    tempCount = 0;

    portHandler      = NULL;
    readPosGroup     = NULL;
    writePosGroup    = NULL;
    readCurrentGroup = NULL;
    readTempGroup    = NULL;

    joint_num = setting.getjointNum();
    std::vector<ST_SERVO_PARAM> list = setting.getServoParam();
    for( j=0 ; j<joint_num ; ++j ){
        JOINT_CONTROL work( list[j].name, list[j].id, list[j].center, list[j].home );
        joints.push_back( work );
    }

    /* DynamixelSDKとros_controlへの接続初期化 */
    packetHandler    = dynamixel::PacketHandler::getPacketHandler( PROTOCOL_VERSION );
    portHandler      = dynamixel::PortHandler::getPortHandler( setting.getPortName().c_str() );
    readPosGroup     = new dynamixel::GroupBulkRead( portHandler, packetHandler );
    writePosGroup    = new dynamixel::GroupBulkWrite( portHandler, packetHandler );
    readTempGroup    = new dynamixel::GroupBulkRead( portHandler, packetHandler );
    readCurrentGroup = new dynamixel::GroupBulkRead( portHandler, packetHandler );
    
    for( j=0 ; j<joint_num ; ++j ){
        uint8_t dxl_id = joints[j].get_dxl_id();
        if( !readPosGroup->addParam( dxl_id, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION ) ){
            last_error = "Bulk pos read setting failed.";
            return;
        }
        if( !writePosGroup->addParam( dxl_id, ADDR_GOAL_POSITION, LEN_GOAL_POSITION, joints[j].get_dxl_goal_addr() ) ){// [TODO]
            last_error = "Bulk pos write setting failed.";
            return;
        }
        if( !readTempGroup->addParam( dxl_id, ADDR_PRESENT_TEMP, LEN_PRESENT_TEMP ) ){
            last_error = "Bulk temp read setting failed.";
            return;
        }
        if( !readCurrentGroup->addParam( dxl_id, ADDR_PRESENT_CURRENT, LEN_PRESENT_CURRENT ) ){
            last_error = "Bulk current read setting failed.";
            return;
        }
    }

    // Open port
    last_error = "";
    if( !portHandler->openPort() ){
        last_error = "Port open failed.";
        port_stat = false;
    }else{
        // Set port baudrate
        if( !portHandler->setBaudRate( setting.getBaudrate() ) ){
            last_error = "Setup baudrate failed.";
            port_stat = false;
        }else{
            for( j=0 ; j<joint_num ; ++j ){
                uint8_t dxl_id = joints[j].get_dxl_id();
                int32_t present_pos = 0;

                dxl_comm_result = packetHandler->read4ByteTxRx(portHandler, dxl_id, ADDR_PRESENT_POSITION, (uint32_t*)&present_pos, &dxl_error);
                if (dxl_comm_result != COMM_SUCCESS){
                    last_error = packetHandler->getTxRxResult( dxl_comm_result );
                    return;
                }else if ( dxl_error != 0 ){
                    last_error = packetHandler->getRxPacketError( dxl_error );
                    return;
                }else{
                    joints[j].set_position( DXLPOS2RAD( present_pos ) );
                }
            }
            port_stat = true;
        }
    }
    for( j=0 ; j<joint_num ; ++j ){
        hardware_interface::JointStateHandle reg_state_handle( joints[j].get_joint_name(), joints[j].get_position_addr(), joints[j].get_velocity_addr(), joints[j].get_effort_addr() );
        joint_stat_if.registerHandle( reg_state_handle );
    }
    registerInterface( &joint_stat_if );

    for( j=0 ; j<joint_num ; ++j ){
        hardware_interface::JointHandle reg_pos_handle( joint_stat_if.getHandle(joints[j].get_joint_name()), joints[j].get_command_addr() );
        joint_pos_if.registerHandle( reg_pos_handle );
    }
    registerInterface( &joint_pos_if );

    init_stat = true;
}

DXLPORT_CONTROL::~DXLPORT_CONTROL()
{
    portHandler->closePort();
	delete( portHandler );
	/* packetHandlerはdeleteしないほうが良さそう*/
    if(readPosGroup!=NULL)     delete( readPosGroup );
    if(readTempGroup!=NULL)    delete( readTempGroup );
    if(writePosGroup!=NULL)    delete( writePosGroup );
    if(readCurrentGroup!=NULL) delete( readCurrentGroup );
}

void DXLPORT_CONTROL::read( ros::Time time, ros::Duration period )
{
    if( !port_stat ){
        return;
    }
    readPos( time, period );
    readCurrent( time, period );
    if( (time - tempTime).toSec() > DXL_TEMP_READ_DURATION ){
        readTemp( time, period );
        tempTime = time;
    }
}

void DXLPORT_CONTROL::readPos( ros::Time time, ros::Duration period )
{
    int dxl_comm_result = COMM_TX_FAIL;             // Communication result
    bool dxl_getdata_result = false;
    uint8_t dxl_error = 0;                          // Dynamixel error

    last_error = "";
    dxl_comm_result = readPosGroup->txRxPacket();
    if (dxl_comm_result != COMM_SUCCESS){
        last_error = packetHandler->getTxRxResult( dxl_comm_result );
        ++rx_err;
    }else{
        for( int j=0 ; j<joint_num ; ++j ){
            int32_t present_pos = 0;
            uint8_t dxl_id = joints[j].get_dxl_id();
            dxl_getdata_result = readPosGroup->isAvailable( dxl_id, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION );
            if( !dxl_getdata_result ){
                ++rx_err;
                break;
            }else{
                present_pos = readPosGroup->getData( dxl_id, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION );
                joints[j].set_dxl_pos( present_pos );
                present_pos = (present_pos - joints[j].get_center());
                joints[j].set_position( DXLPOS2RAD( present_pos ) );
            }
        }
    }
}

void DXLPORT_CONTROL::readCurrent( ros::Time time, ros::Duration period )
{
    int dxl_comm_result = COMM_TX_FAIL;             // Communication result
    bool dxl_getdata_result = false;
    uint8_t dxl_error = 0;                          // Dynamixel error

    last_error = "";
    dxl_comm_result = readCurrentGroup->txRxPacket();
    if (dxl_comm_result != COMM_SUCCESS){
        last_error = packetHandler->getTxRxResult( dxl_comm_result );
        ++rx_err;
    }else{
        for( int j=0 ; j<joint_num ; ++j ){
            int16_t present_current = 0;
            uint8_t dxl_id = joints[j].get_dxl_id();
            dxl_getdata_result = readCurrentGroup->isAvailable( dxl_id, ADDR_PRESENT_CURRENT, LEN_PRESENT_CURRENT );
            if( !dxl_getdata_result ){
                ++rx_err;
                break;
            }else{
                present_current = readCurrentGroup->getData( dxl_id, ADDR_PRESENT_CURRENT, LEN_PRESENT_CURRENT );
                joints[j].set_dxl_curr( present_current );
                joints[j].set_current( (DXL_CURRENT_UNIT * present_current) );
            }
        }
    }
}

void DXLPORT_CONTROL::readTemp( ros::Time time, ros::Duration period )
{
    int dxl_comm_result = COMM_TX_FAIL;             // Communication result
    bool dxl_getdata_result = false;
    uint8_t dxl_error = 0;                          // Dynamixel error
   
    last_error = "";
    dxl_comm_result = readTempGroup->txRxPacket();
    if (dxl_comm_result != COMM_SUCCESS){
        last_error = packetHandler->getTxRxResult( dxl_comm_result );
        ++rx_err;
    }else{
        for( int j=0 ; j<joint_num ; ++j ){
            uint8_t dxl_id = joints[j].get_dxl_id();
            dxl_getdata_result = readTempGroup->isAvailable( dxl_id, ADDR_PRESENT_TEMP, LEN_PRESENT_TEMP );
            if( !dxl_getdata_result ){
                ++rx_err;
                break;
            }else{
                uint8_t present_current = readTempGroup->getData( dxl_id, ADDR_PRESENT_TEMP, LEN_PRESENT_TEMP );
                joints[j].set_dxl_temp( present_current );
                joints[j].set_temprature( present_current );
            }
        }
        ++tempCount;
    }
}

void DXLPORT_CONTROL::write( ros::Time time, ros::Duration period )
{
    int dxl_comm_result = COMM_TX_FAIL;             // Communication result
    uint8_t dxl_error = 0;                          // Dynamixel error

    if( !port_stat){
        for( int j=0 ; j<joint_num ; ++j ){
            joints[j].set_position( joints[j].get_command() );
        }
        return;
    }
    last_error = "";
    for( int j=0 ; j<joint_num ; ++j ){
        double work_pos = RAD2DXLPOS( joints[j].get_command() );
        work_pos += joints[j].get_center();          // ROS(-180 <=> +180) => DXL(0 <=> 4095)
        if( work_pos < DXL_MIN_LIMIT ){
            work_pos = DXL_MIN_LIMIT;
        }
        if( work_pos > DXL_MAX_LIMIT ){
            work_pos = DXL_MAX_LIMIT;
        }

        uint32_t dxl_pos = (uint32_t)round( work_pos );
        uint8_t* goal_data = joints[j].get_dxl_goal_addr();

        goal_data[0] = (uint8_t)(dxl_pos&0x000000FF);
        goal_data[1] = (uint8_t)((dxl_pos&0x0000FF00)>>8);
        goal_data[2] = (uint8_t)((dxl_pos&0x00FF0000)>>16);
        goal_data[3] = (uint8_t)((dxl_pos&0xFF000000)>>24);

        writePosGroup->changeParam( joints[j].get_dxl_id(), ADDR_GOAL_POSITION, LEN_GOAL_POSITION, goal_data );
    }
    dxl_comm_result = writePosGroup->txPacket();
    if( dxl_comm_result != COMM_SUCCESS ){
        last_error = packetHandler->getTxRxResult( dxl_comm_result );
        ++tx_err;
    }else if( dxl_error != 0 ){
        last_error = packetHandler->getRxPacketError( dxl_error );
        ++tx_err;
    }
}

void DXLPORT_CONTROL::set_gain_all( uint16_t gain )
{
    int dxl_comm_result = COMM_TX_FAIL;             // Communication result
    uint8_t dxl_error = 0;                          // Dynamixel error

    if( !port_stat ){
        return;
    }
    last_error = "";
    for( int j=0 ; j<joint_num ; ++j ){
        set_gain( joints[j].get_dxl_id(), gain );
    }
}

void DXLPORT_CONTROL::set_gain( uint8_t dxl_id, uint16_t gain )
{
    int dxl_comm_result = COMM_TX_FAIL;             // Communication result
    uint8_t dxl_error = 0;                          // Dynamixel error

    dxl_comm_result = packetHandler->write2ByteTxRx( portHandler, dxl_id, ADDR_POSITION_PGAIN, gain, &dxl_error );
    if( dxl_comm_result != COMM_SUCCESS ){
        last_error = packetHandler->getTxRxResult( dxl_comm_result );
        ++tx_err;
    }else if( dxl_error != 0 ){
        last_error = packetHandler->getRxPacketError( dxl_error );
        ++tx_err;
    }
}

void DXLPORT_CONTROL::set_torque( bool torque )
{
    int dxl_comm_result = COMM_TX_FAIL;             // Communication result
    uint32_t set_param = torque ? TORQUE_ENABLE:TORQUE_DISABLE;
    uint8_t dxl_error = 0;                          // Dynamixel error

    last_error = "";
    if( !port_stat ){
        return;
    }
    for( int j=0 ; j<joint_num; ++j ){
        dxl_comm_result = packetHandler->write1ByteTxRx( portHandler, joints[j].get_dxl_id(), ADDR_TORQUE_ENABLE, set_param, &dxl_error );
        if( dxl_comm_result != COMM_SUCCESS ){
            last_error = packetHandler->getTxRxResult( dxl_comm_result );
            ++tx_err;
        }else if( dxl_error != 0 ){
            last_error = packetHandler->getRxPacketError( dxl_error );
            ++tx_err;
        }else{
            joints[j].set_torque( torque );
        }
    }
}

/* 起動時モーション */
void DXLPORT_CONTROL::startup_motion( void )
{
    uint8_t dxl_error = 0;                          // Dynamixel error
    ros::Rate rate( DXL_TORQUR_ON_STEP );
    int step_max = DXL_TORQUE_ON_STEP_MAX;
    ros::Time t = getTime();
    ros::Duration d = getDuration(t);
    int step_a, step_b;
    std::vector<ST_HOME_MOTION_DATA> home_motion_data;

    set_torque( true );                             // 全関節トルクON
    set_gain_all( DXL_DEFAULT_PGAIN );

    /* 開始位置取り込みと差分計算 */
    readPos( t, d );
    for( int j=0 ; j<joint_num ; ++j ){
        ST_HOME_MOTION_DATA motion_work;
        motion_work.home      = joints[j].get_home();
        motion_work.home_rad  = DXLPOS2RAD( motion_work.home ) - DXLPOS2RAD( joints[j].get_center() );
        motion_work.start_rad = joints[j].get_position();
        motion_work.start     = RAD2DXLPOS( motion_work.start_rad ) + joints[j].get_center();
        motion_work.step_rad  = 
            (motion_work.home > motion_work.start) ? ((motion_work.home_rad - motion_work.start_rad)/step_max)
                                                   : -((motion_work.start_rad - motion_work.home_rad)/step_max);
        joints[j].set_command( joints[j].get_position() );
        home_motion_data.push_back( motion_work );
    }
    write( t, d );

    /* ホームポジションへ移動する */
    for( int step=0 ; step<step_max ; ++step ){
        d = getDuration(t);
        t = getTime();
        readPos( t, d );
        if( !port_stat ){
            for( int j=0 ; j<joint_num ; ++j ){
                joints[j].set_command( DXLPOS2RAD( joints[j].get_home() ) - DXLPOS2RAD( joints[j].get_center() ) );
            }
            continue;
        }
        for( int j=0 ; j<joint_num ; ++j ){
            /* [TODO]物理的に引っかかっている時に逃げられるよう何か対策を講じた方が良い */
            joints[j].set_command( joints[j].get_command() + home_motion_data[j].step_rad );
        }
        write( t, d );
        rate.sleep();
    }
    /* [TODO]物理的に引っかかっている時に逃げられるよう何か対策を講じた方が良い */
    /* ホームポジションを設定する */
    for( int j=0 ; j<joint_num ; ++j ){
        joints[j].set_command( home_motion_data[j].home_rad );
    }
    write( t, d );
}

/* セルフチェック */
bool DXLPORT_CONTROL::check_servo_param( uint8_t dxl_id, uint32_t test_addr, uint8_t equal )
{
    int dxl_comm_result = COMM_TX_FAIL;             // Communication result
    uint8_t dxl_error = 0;                          // Dynamixel error
    uint8_t read_data;
    bool result = false;

    dxl_comm_result = packetHandler->read1ByteTxRx(portHandler, dxl_id, test_addr, &read_data, &dxl_error);
    if( dxl_comm_result != COMM_SUCCESS ){
        last_error = packetHandler->getTxRxResult( dxl_comm_result );
        ++rx_err;
    }else if( dxl_error != 0 ){
        last_error = packetHandler->getRxPacketError( dxl_error );
        ++rx_err;
    }
    if( read_data == equal ){
        result = true;
    }else{
        // ROS_INFO("%s",std::to_string(read_data).c_str());
        (void)packetHandler->write1ByteTxRx( portHandler, dxl_id, test_addr, equal );
    }
    return result;
}
bool DXLPORT_CONTROL::check_servo_param( uint8_t dxl_id, uint32_t test_addr, uint16_t equal )
{
    int dxl_comm_result = COMM_TX_FAIL;             // Communication result
    uint8_t dxl_error = 0;                          // Dynamixel error
    uint16_t read_data;
    bool result = false;

    dxl_comm_result = packetHandler->read2ByteTxRx(portHandler, dxl_id, test_addr, &read_data, &dxl_error);
    if( dxl_comm_result != COMM_SUCCESS ){
        last_error = packetHandler->getTxRxResult( dxl_comm_result );
        ++rx_err;
    }else if( dxl_error != 0 ){
        last_error = packetHandler->getRxPacketError( dxl_error );
        ++rx_err;
    }
    if( read_data == equal ){
        result = true;
    }else{
        // ROS_INFO("%s",std::to_string(read_data).c_str());
        (void)packetHandler->write2ByteTxRx( portHandler, dxl_id, test_addr, equal );
    }
    return result;
}
bool DXLPORT_CONTROL::check_servo_param( uint8_t dxl_id, uint32_t test_addr, uint32_t equal )
{
    int dxl_comm_result = COMM_TX_FAIL;             // Communication result
    uint8_t dxl_error = 0;                          // Dynamixel error
    uint32_t read_data;
    bool result = false;

    dxl_comm_result = packetHandler->read4ByteTxRx(portHandler, dxl_id, test_addr, &read_data, &dxl_error);
    if( dxl_comm_result != COMM_SUCCESS ){
        last_error = packetHandler->getTxRxResult( dxl_comm_result );
        ++rx_err;
    }else if( dxl_error != 0 ){
        last_error = packetHandler->getRxPacketError( dxl_error );
        ++rx_err;
    }
    if( read_data == equal ){
        result = true;
    }else{
        // ROS_INFO("%s",std::to_string(read_data).c_str());
        (void)packetHandler->write4ByteTxRx( portHandler, dxl_id, test_addr, equal );
    }
    return result;
}

std::string DXLPORT_CONTROL::self_check( void )
{
    int dxl_comm_result = COMM_TX_FAIL;             // Communication result
    uint8_t dxl_error = 0;                          // Dynamixel error
    std::string res_str = "[DYNAMIXEL PARAMETER SELF CHECK]\n";
    uint8_t chk_8data;
    uint16_t chk_16data;
    uint32_t chk_32data;

    if( !port_stat ){
        res_str = "SKIP SELF CHECK...";
        return res_str;
    }
    for( int i=0 ; i<(sizeof(RegTable)/sizeof(ST_DYNAMIXEL_REG_TABLE)) ; ++i ){
        if( RegTable[i].selfcheck ){
            bool check_result = true;
            bool read_result;
            res_str += RegTable[i].name + " test...\n";
            switch( RegTable[i].length ){
            case 1:
                chk_8data = (uint8_t)RegTable[i].init_value;
                for( int j=0 ; j<joint_num ; ++j ){
                    read_result = check_servo_param( joints[j].get_dxl_id(), RegTable[i].address, chk_8data );
                    if( !read_result ){
                        res_str += " ID: " + std::to_string(joints[j].get_dxl_id()) + " check NG\n";
                        check_result = false;
                    }
                }
                break;
            case 2:
                chk_16data = (uint16_t)RegTable[i].init_value;
                for( int j=0 ; j<joint_num ; ++j ){
                    read_result = check_servo_param( joints[j].get_dxl_id(), RegTable[i].address, chk_16data );
                    if( !read_result ){
                        res_str += " ID: " + std::to_string(joints[j].get_dxl_id()) + " check NG\n";
                        check_result = false;
                    }
                }
                break;
            case 4:
                chk_32data = (uint32_t)RegTable[i].init_value;
                for( int j=0 ; j<joint_num ; ++j ){
                    read_result = check_servo_param( joints[j].get_dxl_id(), RegTable[i].address, chk_32data );
                    if( !read_result ){
                        res_str += " ID: " + std::to_string(joints[j].get_dxl_id()) + " check NG\n";
                        check_result = false;
                    }
                }
                break;
            }
            if( check_result ){
                res_str += " CHECK OK\n";
            }else{
                res_str += " CHECK NG!\n";
            }
        }
    }
    return res_str;
}