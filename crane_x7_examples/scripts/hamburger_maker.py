#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import geometry_msgs.msg
import rosnode
from tf.transformations import quaternion_from_euler
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QDialog, QLabel, QHBoxLayout, QVBoxLayout, QCheckBox, QWidget
from PyQt5.QtGui import QPixmap
import math
from darknet_ros_msgs.msg import BoundingBoxes
         
 
total_beef = 2
total_buns_1 = 2
total_buns_2 = 2
total_cheese_beef = 2
total_tomato = 2
total_lettuce = 2
total_onion = 2

def DarknetBboxCallback(darknet_bboxs):
    print('detection')
    bbox = darknet_bboxs.bounding_boxes[0]
    bbox_name = bbox.Class
    if bbox_name == 'paperplate':
        print(bbox.Class)
        app = QApplication(sys.argv)
        ex = Example()
        ex.show()
        sys.exit(app.exec_())


class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        label_1 = QLabel('<h1><font size="8" color="red">ROS BURGER<h1>', self)
        label_1.move(220, 20)
        label_2 = QLabel('<font size="5" color="black">[ FOOD MENU ]', self)
        label_2.move(250, 100)
        label_3 = QLabel('<i><p><font size="5" color="black">Thank you for stopping in! Choose what you like and click!<i></font></p>', self)
        label_3.move(45, 220)

        self.resize(670, 300)
        self.move(300, 300)

        btn1 = QPushButton("Hamburger", self)
        btn1.move(80, 150)

        btn2 = QPushButton("Cheeseburger", self)
        btn2.move(200, 150)

        btn3 = QPushButton("Specialbuger", self)
        btn3.move(340, 150)

        btn4 = QPushButton("CREATE", self)
        btn4.move(480, 150)

        btn1.clicked.connect(self.Push_Hamburger)
        btn2.clicked.connect(self.Push_Cheeseburger)
        btn3.clicked.connect(self.Push_Specialburger)
        btn4.clicked.connect(self.Push_CREATE)


        self.setWindowTitle('Crane_x7_Hamburger_Maker')

    def Push_Hamburger(self):
        hamburger = Hamburger()
        hamburger.show()

    def Push_Cheeseburger(self):
        cheeseburger = Cheeseburger()
        cheeseburger.show()

    def Push_Specialburger(self):
        specialburger = Specialburger()
        specialburger.show()

    def Push_CREATE(self):
        create = CREATE()
        create.show()


class Hamburger(QMainWindow):
    def __init__(self, parent=None):
        super(Hamburger, self).__init__(parent)
        self.w = QDialog(parent)
        label_1 = QLabel('<font size="5" color="black">OK, so that is one "Hamburger". Is that right?', self)
        label_1.move(10, 20)
 
        layout = QVBoxLayout()
        layout.addWidget(label_1)
        self.w.setLayout(layout)
        self.w.setWindowTitle('Hamburger')

        self.w.setGeometry(500, 400, 390, 150)

 
        self.button = QPushButton('OK', self)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.main)
        self.button.clicked.connect(self.w.close)
 
                             
                                                       
    def show(self):
        self.w.exec_()


    def main(self):
        food_stock = Food_Stock()
        food_stock.buns_1(1)
        food_stock.lettuce(1)
        food_stock.beef(1)
#        food_stock.tomato(1)
        food_stock.onion(1)
        food_stock.buns_2(1)


class Cheeseburger(QMainWindow):
    def __init__(self, parent=None):
        super(Cheeseburger, self).__init__(parent)
        self.w = QDialog(parent)
        label_1 = QLabel('<font size="5" color="black">OK, so that is one "Cheeseburger". Is that right?', self)
        label_1.move(10, 20)
 
        layout = QVBoxLayout()
        layout.addWidget(label_1)
        self.w.setLayout(layout)
        self.w.setWindowTitle('Cheeseburger')

        self.w.setGeometry(500, 400, 390, 150)

 
        self.button = QPushButton('OK', self)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.main)
        self.button.clicked.connect(self.w.close)
 


    def show(self):
        self.w.exec_()


    def main(self):
        food_stock = Food_Stock()
        food_stock.buns_1(1)
        food_stock.lettuce(1)
        food_stock.cheese_beef(1)
#        food_stock.tomato(1)
        food_stock.onion(1)
        food_stock.buns_2(1)
            

class Specialburger(QMainWindow):
    def __init__(self, parent=None):
        super(Specialburger, self).__init__(parent)
        self.w = QDialog(parent)
        label_1 = QLabel('<font size="5" color="black">OK, so that is one "Specialburger". Is that right?', self)
        label_1.move(10, 20)
 
        layout = QVBoxLayout()
        layout.addWidget(label_1)
        self.w.setLayout(layout)
        self.w.setWindowTitle('Specialburger')

        self.w.setGeometry(500, 400, 390, 150)

 
        self.button = QPushButton('OK', self)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.main)
        self.button.clicked.connect(self.w.close)
 
                             
                                                       
    def show(self):
        self.w.exec_()


    def main(self):
        food_stock = Food_Stock()
        food_stock.buns_1(1)
        food_stock.lettuce(1)
        food_stock.cheese_beef(1)
        food_stock.beef(1)
#        food_stock.tomato(1)
        food_stock.onion(1)
        food_stock.buns_2(1)
 


class CREATE(QMainWindow):
    def __init__(self, parent=None):
        super(CREATE, self).__init__(parent)
        self.w = QDialog(parent)
        label = QLabel()
        label.setText('Please choose anything you like !')

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.w.setLayout(layout)
        self.w.setWindowTitle('CREATE')

        self.w.setGeometry(500, 400, 390, 250)

        self.upper_1 = QCheckBox('Lettuce', self)
        layout.addWidget(self.upper_1)

        self.upper_2 = QCheckBox('beef', self)
        layout.addWidget(self.upper_2)

        self.upper_3 = QCheckBox('Cheese on beef', self)
        layout.addWidget(self.upper_3)

#        self.upper_4 = QCheckBox('tomato', self)
#        layout.addWidget(self.upper_4)

        self.upper_5 = QCheckBox('onion', self)
        layout.addWidget(self.upper_5)
 
        self.button = QPushButton('OK', self)
        layout.addWidget(self.button)
        self.button.clicked.connect(self.main)
        self.button.clicked.connect(self.w.close)
 

                             
                                                       
    def show(self):
        self.w.exec_()


    def main(self):
        food_stock = Food_Stock()
        food_stock.buns_1(1)
        if(self.upper_1.isChecked()):
            food_stock.lettuce(1)
        if(self.upper_2.isChecked()):
            food_stock.beef(1)
        if(self.upper_3.isChecked()):
            food_stock.cheese_beef(1)
#        if(self.upper_4.isChecked()):
#            food_stock.tomato(1)
        if(self.upper_5.isChecked()):
            food_stock.onion(1)
        food_stock.buns_2(1)
        



class Food_Stock:
    def beef(self, order):
        global total_beef
        total_beef -= order
        if(total_beef >= 0 and total_buns_1 >= 0):
            print("beef ok!")
            print(total_beef)
        else:
            print("error!! Lack of beef")
            return
        
        
        robot = moveit_commander.RobotCommander()
        arm = moveit_commander.MoveGroupCommander("arm")
        arm.set_max_velocity_scaling_factor(0.5)
        gripper = moveit_commander.MoveGroupCommander("gripper")
    
        while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
            rospy.sleep(1.0)
        rospy.sleep(1.0)
    
        print("Group names:")
        print(robot.get_group_names())
    
        print("Current state:")
        print(robot.get_current_state())
    
    
    
        # アーム初期ポーズを表示
        arm_initial_pose = arm.get_current_pose().pose
        print("Arm initial pose:")
        print(arm_initial_pose)
    
        # ハンドを開く/ 閉じる
        def move_gripper(pou):
            gripper.set_joint_value_target([pou, pou])
            gripper.go()
    
    
        # アームを移動する
        def move_arm(pos_x, pos_y, pos_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(-math.pi/2.0, math.pi/2.0, 0.0)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行
   
        def rotate_hand(pos_x, pos_y, pos_z, euler_x, euler_y, euler_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(euler_x, euler_y, euler_z)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行



        # SRDFに定義されている"home"の姿勢にする
        arm.set_named_target("home")
        arm.go()
         
        #ハンドを開く
        move_gripper(1.3)


        if(total_beef == 1):
            #掴む準備をする
            # SRDFに定義されている"home2"の姿勢にする
            arm.set_named_target("home2")
            arm.go()
        
            #掴みに行く
            arm.set_max_velocity_scaling_factor(0.1)
            move_arm(0.147, 0.3, 0.315)
        
            #ハンドを閉じる
            move_gripper(0.02)
            
            #持ち上げる
            move_arm(0.147, 0.1, 0.35)
        
            #homeに戻る
            arm.set_named_target("home")
            arm.go()
                

        elif(total_beef == 0):
            #掴む準備をする
            # SRDFに定義されている"home2"の姿勢にする
            arm.set_named_target("home2")
            arm.go()
        
            #掴みに行く
            arm.set_max_velocity_scaling_factor(0.1)
            move_arm(0.052, 0.3, 0.315)
        
            #ハンドを閉じる
            move_gripper(0.02)
            
            #持ち上げる
            move_arm(0.052, 0.1, 0.35)
        
            #homeに戻る
            arm.set_named_target("home")
            arm.go()
     
        #下ろす
        rotate_hand(0.30, 0.0, 0.168, 0.0, math.pi/2.0, 0.0)
    
        #少しだけハンドを持ち上げる
        rotate_hand(0.25, 0.0, 0.14, 0.0, math.pi/2.0, 0.0)
 
        #ハンドを開く
        move_gripper(0.5)
    
        #少しだけハンドを持ち上げる
        rotate_hand(0.15, 0.0, 0.19, 0.0, math.pi/2.0, 0.0)
 
        #homeに戻る
        arm.set_named_target("home")
        arm.go()
    
        print("done")


    def buns_1(self, order):
        global total_buns_1
        total_buns_1 -= order
        if(total_buns_1 >= 0):
            print("buns ok!")
            print(total_buns_1)
        else:
            print("error!! Lack of buns")
            return
        
        robot = moveit_commander.RobotCommander()
        arm = moveit_commander.MoveGroupCommander("arm")
        arm.set_max_velocity_scaling_factor(0.5)
        gripper = moveit_commander.MoveGroupCommander("gripper")
    
        while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
            rospy.sleep(1.0)
        rospy.sleep(1.0)
    
        print("Group names:")
        print(robot.get_group_names())
    
        print("Current state:")
        print(robot.get_current_state())
    
    
    
        # アーム初期ポーズを表示
        arm_initial_pose = arm.get_current_pose().pose
        print("Arm initial pose:")
        print(arm_initial_pose)
    
        # ハンドを開く/ 閉じる
        def move_gripper(pou):
            gripper.set_joint_value_target([pou, pou])
            gripper.go()
    
    
        # アームを移動する
        def move_arm(pos_x, pos_y, pos_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(math.pi, 0, 0)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行
   
        def rotate_hand(pos_x, pos_y, pos_z, euler_x, euler_y, euler_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(euler_x, euler_y, euler_z)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行



        # SRDFに定義されている"home"の姿勢にする
        arm.set_named_target("home")
        arm.go()
         
        #ハンドを開く
        move_gripper(1.3)

        if(total_buns_1 == 1 or total_buns_1 == 0):
            #掴む準備をする
            # SRDFに定義されている"home5"の姿勢にする
            arm.set_named_target("home5")
            arm.go()
        
            #掴みに行く
            arm.set_max_velocity_scaling_factor(0.1)
            move_arm(0.035, -0.305, 0.19)
        
            #ハンドを閉じる
            move_gripper(0.01)
            
            #持ち上げる
            move_arm(0.035, -0.305, 0.32)
        
            #homeに戻る
            arm.set_named_target("home")
            arm.go()
 

        #下ろす
        rotate_hand(0.30, 0.0, 0.168, 0.0, math.pi/2.0, 0.0)
    
        #少しだけハンドを持ち上げる
        rotate_hand(0.25, 0.0, 0.14, 0.0, math.pi/2.0, 0.0)
 
        #ハンドを開く
        move_gripper(0.5)
    
        #少しだけハンドを持ち上げる
        rotate_hand(0.15, 0.0, 0.19, 0.0, math.pi/2.0, 0.0)
    
        print("done")


    def buns_2(self, order):
        global total_buns_2
        total_buns_2 -= order
        if(total_buns_2 >= 0 and total_buns_1 >= 0):
            print("buns ok!")
            print(total_buns_2)
        else:
            print("error!! Lack of buns")
            return
        
        robot = moveit_commander.RobotCommander()
        arm = moveit_commander.MoveGroupCommander("arm")
        arm.set_max_velocity_scaling_factor(0.5)
        gripper = moveit_commander.MoveGroupCommander("gripper")
    
        while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
            rospy.sleep(1.0)
        rospy.sleep(1.0)
    
        print("Group names:")
        print(robot.get_group_names())
    
        print("Current state:")
        print(robot.get_current_state())
    
    
    
        # アーム初期ポーズを表示
        arm_initial_pose = arm.get_current_pose().pose
        print("Arm initial pose:")
        print(arm_initial_pose)
    
        # ハンドを開く/ 閉じる
        def move_gripper(pou):
            gripper.set_joint_value_target([pou, pou])
            gripper.go()
    
    
        # アームを移動する
        def move_arm(pos_x, pos_y, pos_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(math.pi, 0, 0)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行
   
        def rotate_hand(pos_x, pos_y, pos_z, euler_x, euler_y, euler_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(euler_x, euler_y, euler_z)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行



        # SRDFに定義されている"home"の姿勢にする
        arm.set_named_target("home")
        arm.go()
         
        #ハンドを開く
        move_gripper(1.3)

        if(total_buns_2 == 0 or total_buns_2 == 1):
            #掴む準備をする
            # SRDFに定義されている"home5"の姿勢にする
            arm.set_named_target("home5")
            arm.go()
        
            #掴みに行く
            arm.set_max_velocity_scaling_factor(0.1)
            move_arm(0.14, -0.305, 0.19)
        
            #ハンドを閉じる
            move_gripper(0.01)
            
            #持ち上げる
            move_arm(0.14, -0.305, 0.32)
        
            #homeに戻る
            arm.set_named_target("home")
            arm.go()
                

        #下ろす
        rotate_hand(0.30, 0.0, 0.168, 0.0, math.pi/2.0, 0.0)
    
        #少しだけハンドを持ち上げる
        rotate_hand(0.25, 0.0, 0.14, 0.0, math.pi/2.0, 0.0)
 
        #ハンドを開く
        move_gripper(0.5)
    
        #少しだけハンドを持ち上げる
        rotate_hand(0.15, 0.0, 0.19, 0.0, math.pi/2.0, 0.0)
    
        print("done")




    def cheese_beef(self, order):
        global total_cheese_beef
        total_cheese_beef -= order
        if(total_cheese_beef >= 0 and total_buns_1 >= 0):
            print("cheese_beef ok!")
            print(total_cheese_beef)
        else:
            print("error!! Lack of cheese_beef")
            return
        
        robot = moveit_commander.RobotCommander()
        arm = moveit_commander.MoveGroupCommander("arm")
        arm.set_max_velocity_scaling_factor(0.5)
        gripper = moveit_commander.MoveGroupCommander("gripper")
    
        while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
            rospy.sleep(1.0)
        rospy.sleep(1.0)
    
        print("Group names:")
        print(robot.get_group_names())
    
        print("Current state:")
        print(robot.get_current_state())
    
    
    
        # アーム初期ポーズを表示
        arm_initial_pose = arm.get_current_pose().pose
        print("Arm initial pose:")
        print(arm_initial_pose)
    
        # ハンドを開く/ 閉じる
        def move_gripper(pou):
            gripper.set_joint_value_target([pou, pou])
            gripper.go()
    
    
        # アームを移動する
        def move_arm(pos_x, pos_y, pos_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(-math.pi/2.0, math.pi/2.0, 0.0)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行
   
        def rotate_hand(pos_x, pos_y, pos_z, euler_x, euler_y, euler_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(euler_x, euler_y, euler_z)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行



        # SRDFに定義されている"home"の姿勢にする
        arm.set_named_target("home")
        arm.go()
         
        #ハンドを開く
        move_gripper(1.3)

        if(total_cheese_beef == 1):
            #掴む準備をする
            # SRDFに定義されている"home2"の姿勢にする
            arm.set_named_target("home2")
            arm.go()
        
            #掴みに行く
            arm.set_max_velocity_scaling_factor(0.1)
            move_arm(-0.053, 0.3, 0.315)
        
            #ハンドを閉じる
            move_gripper(0.02)
            
            #持ち上げる
            move_arm(-0.053, 0.25, 0.35)
        
            #homeに戻る
            arm.set_named_target("home")
            arm.go()
 

        elif(total_cheese_beef == 0):
            #掴む準備をする
            # SRDFに定義されている"home2"の姿勢にする
            arm.set_named_target("home2")
            arm.go()
        
            #掴みに行く
            arm.set_max_velocity_scaling_factor(0.1)
            move_arm(-0.148, 0.3, 0.315)
        
            #ハンドを閉じる
            move_gripper(0.04)
            
            #持ち上げる
            move_arm(-0.148, 0.25, 0.4)
        
            #homeに戻る
            arm.set_named_target("home")
            arm.go()
                

        #下ろす
        rotate_hand(0.30, 0.0, 0.168, 0.0, math.pi/2.0, 0.0)
        
        #少しだけハンドを持ち上げる
        rotate_hand(0.25, 0.0, 0.14, 0.0, math.pi/2.0, 0.0)
 
        #ハンドを開く
        move_gripper(0.5)
 
        #少しだけハンドを持ち上げる
        rotate_hand(0.15, 0.0, 0.19, 0.0, math.pi/2.0, 0.0)
    
        #homeに戻る
        arm.set_named_target("home")
        arm.go()
    
        print("done")

   
    def tomato(self, order):
        global total_tomato
        total_tomato -= order
        if(total_tomato >= 0 and total_buns_1 >= 0):
            print("tomato ok!")
            print(total_tomato)
        else:
            print("error!! Lack of tomato")
            return
        
        
        robot = moveit_commander.RobotCommander()
        arm = moveit_commander.MoveGroupCommander("arm")
        arm.set_max_velocity_scaling_factor(0.5)
        gripper = moveit_commander.MoveGroupCommander("gripper")
    
        while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
            rospy.sleep(1.0)
        rospy.sleep(1.0)
    
        print("Group names:")
        print(robot.get_group_names())
    
        print("Current state:")
        print(robot.get_current_state())
    
    
    
        # アーム初期ポーズを表示
        arm_initial_pose = arm.get_current_pose().pose
        print("Arm initial pose:")
        print(arm_initial_pose)
    
        # ハンドを開く/ 閉じる
        def move_gripper(pou):
            gripper.set_joint_value_target([pou, pou])
            gripper.go()
    
    
        # アームを移動する
        def move_arm(pos_x, pos_y, pos_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(-math.pi/2.0, math.pi/2.0, 0.0)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行
   
        def rotate_hand(pos_x, pos_y, pos_z, euler_x, euler_y, euler_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(euler_x, euler_y, euler_z)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行



        # SRDFに定義されている"home"の姿勢にする
        arm.set_named_target("home")
        arm.go()
         
        #ハンドを開く
        move_gripper(1.3)

        if(total_tomato == 1):
            #掴む準備をする
            # SRDFに定義されている"home2"の姿勢にする
            arm.set_named_target("home2")
            arm.go()
        
            #掴みに行く
            arm.set_max_velocity_scaling_factor(0.1)
            move_arm(0.147, 0.3, 0.215)
        
            #ハンドを閉じる
            move_gripper(0.02)
            
            #持ち上げる
            move_arm(0.147, 0.1, 0.25)
        
            #homeに戻る
            arm.set_named_target("home")
            arm.go()
                

        elif(total_tomato == 0):
            #掴む準備をする
            # SRDFに定義されている"home2"の姿勢にする
            arm.set_named_target("home2")
            arm.go()
        
            #掴みに行く
            arm.set_max_velocity_scaling_factor(0.1)
            move_arm(0.052, 0.3, 0.215)
        
            #ハンドを閉じる
            move_gripper(0.02)
            
            #持ち上げる
            move_arm(0.052, 0.1, 0.25)
        
            #homeに戻る
            arm.set_named_target("home")
            arm.go()
     
        #下ろす
        rotate_hand(0.30, 0.0, 0.168, 0.0, math.pi/2.0, 0.0)
    
        #少しだけハンドを持ち上げる
        rotate_hand(0.25, 0.0, 0.14, 0.0, math.pi/2.0, 0.0)

        #ハンドを開く
        move_gripper(0.5)
 
        #少しだけハンドを持ち上げる
        rotate_hand(0.15, 0.0, 0.19, 0.0, math.pi/2.0, 0.0)
   
        #homeに戻る
        arm.set_named_target("home")
        arm.go()
    
        print("done")

   
    def lettuce(self, order):
        global total_lettuce
        total_lettuce -= order
        if(total_lettuce >= 0 and total_buns_1 >= 0):
            print("lettuce ok!")
            print(total_lettuce)
        else:
            print("error!! Lack of lettuce")
            return
        
        robot = moveit_commander.RobotCommander()
        arm = moveit_commander.MoveGroupCommander("arm")
        arm.set_max_velocity_scaling_factor(0.5)
        gripper = moveit_commander.MoveGroupCommander("gripper")
    
        while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
            rospy.sleep(1.0)
        rospy.sleep(1.0)
    
        print("Group names:")
        print(robot.get_group_names())
    
        print("Current state:")
        print(robot.get_current_state())
    
    
    
        # アーム初期ポーズを表示
        arm_initial_pose = arm.get_current_pose().pose
        print("Arm initial pose:")
        print(arm_initial_pose)
    
        # ハンドを開く/ 閉じる
        def move_gripper(pou):
            gripper.set_joint_value_target([pou, pou])
            gripper.go()
    
    
        # アームを移動する
        def move_arm(pos_x, pos_y, pos_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(-math.pi/2.0, math.pi/2.0, 0.0)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行
   
        def rotate_hand(pos_x, pos_y, pos_z, euler_x, euler_y, euler_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(euler_x, euler_y, euler_z)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行



        # SRDFに定義されている"home"の姿勢にする
        arm.set_named_target("home")
        arm.go()
         
        #ハンドを開く
        move_gripper(1.3)

        if(total_lettuce == 1):
            #掴む準備をする
            # SRDFに定義されている"home2"の姿勢にする
            arm.set_named_target("home2")
            arm.go()
        
            #掴みに行く
            arm.set_max_velocity_scaling_factor(0.1)
            move_arm(-0.053, 0.3, 0.18)
        
            #ハンドを閉じる
            move_gripper(0.01)
            
            #持ち上げる
            move_arm(-0.053, 0.15, 0.25)
        
            #homeに戻る
            arm.set_named_target("home")
            arm.go()
 

        elif(total_lettuce == 0):
            #掴む準備をする
            # SRDFに定義されている"home2"の姿勢にする
            arm.set_named_target("home2")
            arm.go()
        
            #掴みに行く
            arm.set_max_velocity_scaling_factor(0.1)
            move_arm(-0.148, 0.3, 0.215)
        
            #ハンドを閉じる
            move_gripper(0.01)
            
            #持ち上げる
            move_arm(-0.148, 0.15, 0.25)
        
            #homeに戻る
            arm.set_named_target("home")
            arm.go()
                

        #下ろす
        rotate_hand(0.29, 0.0, 0.18, 0.0, math.pi, 0.0)

        #ハンドを開く
        move_gripper(0.5)
 
        #少しだけハンドを持ち上げる
        rotate_hand(0.35, 0.0, 0.19, 0.0, math.pi, 0.0)

        #少しだけハンドを持ち上げる
        rotate_hand(0.40, 0.0, 0.25, 0.0, math.pi, 0.0)
    
        #homeに戻る
        arm.set_named_target("home")
        arm.go()
    
        print("done")


    def onion(self, order):
        global total_onion
        total_onion -= order
        if(total_onion >= 0 and total_buns_1 >= 0):
            print("onion ok!")
            print(total_onion)
        else:
            print("error!! Lack of onion")
            return
        
        robot = moveit_commander.RobotCommander()
        arm = moveit_commander.MoveGroupCommander("arm")
        arm.set_max_velocity_scaling_factor(0.5)
        gripper = moveit_commander.MoveGroupCommander("gripper")
    
        while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
            rospy.sleep(1.0)
        rospy.sleep(1.0)
    
        print("Group names:")
        print(robot.get_group_names())
    
        print("Current state:")
        print(robot.get_current_state())
    
    
    
        # アーム初期ポーズを表示
        arm_initial_pose = arm.get_current_pose().pose
        print("Arm initial pose:")
        print(arm_initial_pose)
    
        # ハンドを開く/ 閉じる
        def move_gripper(pou):
            gripper.set_joint_value_target([pou, pou])
            gripper.go()
    
    
        # アームを移動する
        def move_arm(pos_x, pos_y, pos_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(-math.pi/2.0, 0.0, 0.0)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行
   
        def rotate_hand(pos_x, pos_y, pos_z, euler_x, euler_y, euler_z):
            target_pose = geometry_msgs.msg.Pose()
            target_pose.position.x = pos_x
            target_pose.position.y = pos_y
            target_pose.position.z = pos_z
            q = quaternion_from_euler(euler_x, euler_y, euler_z)  
            target_pose.orientation.x = q[0]
            target_pose.orientation.y = q[1]
            target_pose.orientation.z = q[2]
            target_pose.orientation.w = q[3]
            arm.set_pose_target(target_pose)  # 目標ポーズ設定
            arm.go()  # 実行



        # SRDFに定義されている"home"の姿勢にする
        arm.set_named_target("home")
        arm.go()
         
        #ハンドを開く
        move_gripper(1.3)

        if(total_onion == 1):
            #掴む準備をする
            # SRDFに定義されている"home4"の姿勢にする
            arm.set_named_target("home4")
            arm.go()
            move_arm(0.147, 0.3, 0.15)
        
            #掴みに行く
            arm.set_max_velocity_scaling_factor(0.1)
            move_arm(0.147, 0.4, 0.055)
        
            #ハンドを閉じる
            move_gripper(0.29)
            
            #持ち上げる
            move_arm(0.147, 0.25, 0.055)
        
            # SRDFに定義されている"home3"の姿勢にする
            arm.set_named_target("home3")
            arm.go()
                

        elif(total_onion == 0):
            #掴む準備をする
            # SRDFに定義されている"home4"の姿勢にする
            arm.set_named_target("home4")
            arm.go()
            move_arm(0.052, 0.3, 0.15)
        
            #掴みに行く
            arm.set_max_velocity_scaling_factor(0.1)
            move_arm(0.052, 0.4, 0.055)
        
            #ハンドを閉じる
            move_gripper(0.29)
            
            #持ち上げる
            move_arm(0.052, 0.25, 0.055)
        
            # SRDFに定義されている"home3"の姿勢にする
            arm.set_named_target("home3")
            arm.go()
     
    
        #下ろす
        rotate_hand(0.30, -0.05, 0.25, -math.pi/2.0, 0.0, -math.pi/2.0)

        #ハンドを回転
        arm.set_max_velocity_scaling_factor(0.1)
        rotate_hand(0.28, 0.03, 0.25, -math.pi/2.0, math.pi/3.0, -math.pi/2.0)
        rotate_hand(0.28, 0.03, 0.2, -math.pi/2.0, math.pi/1.2, -math.pi/2.0)

        arm.set_max_velocity_scaling_factor(0.5)
        
        #少しだけハンドを持ち上げる
        rotate_hand(0.28, 0.03, 0.25, -math.pi/2.0, math.pi/1.2, -math.pi/2.0)
        rotate_hand(0.28, 0.03, 0.2, -math.pi/2.0, math.pi/1.2, -math.pi/2.0)
        rotate_hand(0.28, 0.03, 0.25, -math.pi/2.0, math.pi/1.2, -math.pi/2.0)
        rotate_hand(0.28, 0.03, 0.2, -math.pi/2.0, math.pi/1.2, -math.pi/2.0)

        # SRDFに定義されている"home3"の姿勢にする
        arm.set_named_target("home3")
        arm.go()
        rotate_hand(-0.2, -0.3, 0.3, math.pi/2.0, math.pi, 0.0)
        move_gripper(1.0)
        move_gripper(0.29)
        #homeに戻る
        arm.set_named_target("home")
        arm.go()
    
        print("done")




if __name__ == '__main__':

    try:
        if not rospy.is_shutdown():
            rospy.init_node("crane_x7_make_hamburger")
            rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, DarknetBboxCallback)
            rospy.spin()

    except rospy.ROSInterruptException:
        pass
