# crane_x7_examples

CRANE-X7のためのパッケージ、 `crane_x7` で用いるサンプルをまとめたパッケージです。

## システムの起動方法

CRANE-X7の制御信号ケーブルを制御用パソコンへ接続します。
Terminalを開き、`crane_x7_bringup`の`demo.launch`を起動します。
このlaunchファイルには次のオプションが用意されています。

- fake_execution (default: true)

実機を使用する/使用しない

### シミュレータを使う場合

実機無しで動作を確認する場合、
制御信号ケーブルを接続しない状態で次のコマンドを実行します。

```sh
roslaunch crane_x7_bringup demo.launch fake_execution:=true
```

### 実機を使う場合

実機で動作を確認する場合、
制御信号ケーブルを接続した状態で次のコマンドを実行します。

```sh
roslaunch crane_x7_bringup demo.launch fake_execution:=false
```

ケーブルの接続ポート名はデフォルトで`/dev/ttyUSB0`です。
別のポート名(例: /dev/ttyUSB1)を使う場合は次のコマンドを実行します。

```sh
roslaunch crane_x7_bringup demo.launch fake_execution:=false port:=/dev/ttyUSB1
```

### Gazeboを使う場合

次のコマンドで起動します。実機との接続やcrane_x7_bringupの実行は必要ありません。

```sh
roslaunch crane_x7_gazebo crane_x7_with_table.launch
```

## プログラムの実行方法

`demo.launch`を実行している状態で各プログラムを実行することができます。


### hamburger_maker.pyの実行
千葉工業大学の講義「ロボット設計製作論実習３」の最終発表で使ったコードです。

紙皿を認識して、ハンバーガーの盛り付けを行います。

紙皿を認識させるとGUIが表示され、実行するものをcrane_X7に注文することができます。

詳しくは[こちら](https://github.com/GakuKuwano/crane_x7_ros/blob/master/crane_x7_examples/ROS_BURGER.pdf)を参照してください。

### <インストールするもの>

・RealSense ROSをインストールする

　　詳しくは[こちら](https://github.com/IntelRealSense/realsense-ros)を参照してください。

・darknet_rosをインストールする

　　詳しくは[こちら](https://github.com/leggedrobotics/darknet_ros)を参照してください。

・PyQtをインストールする

```sh
pip install PyQt5
```

　　詳しくは[こちら](https://www.riverbankcomputing.com/static/Docs/PyQt5/installation.html)を参照してください。

### <実行方法>

まず、RealSenseカメラの起動をするために次のコマンドを実行します。

```sh
roslaunch realsense2_camera rs_camera.launch
```

さらに、darknet_rosの起動をするために次のコマンドを実行します。

```sh
roslaunch darknet_ros darknet_ros.launch
```

paper_plateの認識結果

![Figure_darknet](https://github.com/GakuKuwano/crane_x7_ros/blob/master/crane_x7_examples/predictions.jpg "Figure_darknet")


最後に、次のコマンドを実行します。

```sh
rosrun crane_x7_examples hamburger_maker.py
```

皿を認識したら以下のようなGUIが表示されます。好きなボタンを選んで押すと、注文することができます。

![Figure_GUI](https://github.com/GakuKuwano/crane_x7_ros/blob/master/crane_x7_examples/Screenshot%20from%202020-01-27%2003-05-57.png "Figure_GUI")

**実機を使う場合**

### <具材のサイズ>

buns上：直径100mm, 厚さ30mm 

buns下：直径100mm, 厚さ15mm

beef：直径95mm, 厚さ5mm

cheese：80×80mm

紙コップ：高さ60mm, 上部φ55mm, 下部φ40mm, 

紙皿：120×120mm

### <全体図>

![Figure_hamburger](https://github.com/GakuKuwano/crane_x7_ros/blob/master/crane_x7_examples/ROS_BURGER_ZAHYO.png "Figure_hamburger")

### <棚に具材を置く位置>

![Figure2_hamburger](https://github.com/GakuKuwano/crane_x7_ros/blob/master/crane_x7_examples/ROS_BURGER_ZAHYO2.png "Figure2_hamburger")

### <バンズを置く位置>

![Figure3_hamburger](https://github.com/GakuKuwano/crane_x7_ros/blob/master/crane_x7_examples/ROS_BURGER_ZAHYO3.png "Figure3_hamburger")

動作させると[こちら](https://youtu.be/36TV19ttN3A)のような動きをします。

---

### papercup_tower.pyの実行

千葉工業大学の講義「ロボット設計製作論実習３」で中間発表で使ったコードです。

紙コップを掴んで運び、４段ピラミッドを作ります。

次のコマンドを実行します。

```sh
rosrun crane_x7_examples papercup_tower.py
```

![papercup_tower](https://i.imgur.com/TuRv7Qe.jpg "papercup_tower")

**実機を使う場合**

紙コップの寸法：高さ60mm, 上部φ55mm, 下部φ40mm

紙コップを置く位置は以下の図です。紙コップは逆さまにして置きます。詳しくは[こちらのソースコード](https://github.com/GakuKuwano/crane_x7_ros/blob/master/crane_x7_gazebo/worlds/table2.world)に書いてあります。

![Figure_papercup](https://i.imgur.com/mxhpEtP.png "Figure_papercup")

動作させると[こちら](https://www.youtube.com/watch?v=9H0dxWXuLgc)のような動きをします。

---

## サンプルの実行方法

`demo.launch`を実行している状態で各サンプルを実行することができます。

### gripper_action_example.pyの実行

ハンドを開閉させるコード例です。
このサンプルは実機動作のみに対応しています。

次のコマンドで45度まで開いて閉じる動作を実行します。

```sh
rosrun crane_x7_examples gripper_action_example.py
```

---

### pose_groupstate_example.pyの実行

group_stateを使うコード例です。

SRDFファイル[crane_x7_moveit_config/config/crane_x7.srdf](../crane_x7_moveit_config/config/crane_x7.srdf)
に記載されている`home`と`vertical`の姿勢に移行します。

次のコマンドを実行します。

```sh
rosrun crane_x7_examples pose_groupstate_example.py
```

---

### crane_x7_pick_and_place_demo.pyの実行

モノを掴む・持ち上げる・運ぶ・置くコード例です。

次のコマンドを実行します。

```sh
rosrun crane_x7_examples crane_x7_pick_and_place_demo.py
```

![bringup_rviz](https://github.com/rt-net/crane_x7_ros/blob/images/images/bringup_rviz.gif "bringup_rviz")

**実機を使う場合**

CRANE-X7から20cm離れた位置にピッキング対象を設置します。

![bringup](https://github.com/rt-net/crane_x7_ros/blob/images/images/bringup.jpg "bringup")

サンプルで使用しているこのオレンジ色のソフトボールはRT ROBOT SHOPの[こちらのページ](https://www.rt-shop.jp/index.php?main_page=product_info&cPath=1299_1307&products_id=3701)から入手することができます。

動作させると[こちら](https://youtu.be/_8xBgpgMhk8)のような動きになります。

---

### preset_pid_gain_example.pyの実行

`crane_x7_control`の`preset_reconfigure`を使うコード例です。
サーボモータのPIDゲインを一斉に変更できます。

プリセットは[crane_x7_control/scripts/preset_reconfigure.py](../crane_x7_control/scripts/preset_reconfigure.py)
にて編集できます。

次のコマンドを実行すると、`preset_reconfigure.py`と`preset_pid_gain_example.py`のノードを起動します。

```sh
roslaunch crane_x7_examples preset_pid_gain_example.launch
```

動作させると[こちら](https://youtu.be/0rBbgNDwm6Y)のような動きになります。

---

### teaching_example.pyの実行

ティーチングのコード例です。X7のPIDゲインを小さくすることでダイレクトティーチングができます。

次のコマンドでノードを起動します。

```sh
roslaunch crane_x7_examples teaching_example.launch
```

以下のキー割当を参考に、キーボードから操作してください。

**Teaching Mode**

起動時のモードです。トルクOFF*状態です。

| キー | 機能 |
----|----
| s / S | 現在の姿勢を保存 |
| d / D | これまでに保存した姿勢を削除 |
| m / M | **Action Mode**へ遷移 |
| q / Q | シャットダウン |


**Action Mode**

Teaching Modeから遷移します。トルクON*状態です。

| キー | 機能 |
----|----
| p / P | 保存した姿勢を１つずつ再生 |
| a / A | 保存した姿勢のすべてを連続再生 |
| l / L | ループ再生 ON / OFF |
| m / M | **Teaching Mode**へ遷移 |
| q / Q | シャットダウン |

- トルクのON / OFFはサーボモータのPIDゲインに小さい値をプリセットすることで実現しています。

動作させると[こちら](https://youtu.be/--5_l1DpQ-0)のような動きになります。

---

### joystick_example.pyの実行

ジョイスティックでX7を動かすコード例です。
手先の位置・姿勢の変更、グリッパーの開閉、PIDゲインのプリセット、ティーチングができます。

ジョイスティックをPCに接続し、`/dev/input/js0`が存在することを確認してください。

次のコマンドでノードを起動します。

#### 実機を使う場合

```sh
roslaunch crane_x7_examples joystick_example.launch
```

#### シミュレータを使う場合

シミュレータを使う場合は、エラーを防ぐため`sim`オプションを追加してください。

```sh
roslaunch crane_x7_examples joystick_example.launch sim:=true
```

#### キー割り当ての変更

デフォルトのキー割り当てはこちらです。ジョイスティックは
[Logicool Wireless Gamepad F710](https://support.logicool.co.jp/ja_jp/product/wireless-gamepad-f710)
を使っています。
![key_config](https://github.com/rt-net/crane_x7_ros/blob/images/images/joystick_example_key_config.png "key_config")

[crane_x7_example/launch/joystick_example.launch](./launch/joystick_example.launch)
のキー番号を編集することで、キー割り当てを変更できます。

```xml
 <node name="joystick_example" pkg="crane_x7_examples" type="joystick_example.py" required="true" output="screen">
    <!-- 使用するジョイスティックコントローラに合わせてvalueを変更してください -->
    <!-- ひとつのボタンに複数の機能を割り当てています -->
    <param name="button_shutdown_1" value="8" type="int" />
    <param name="button_shutdown_2" value="9" type="int" />

    <param name="button_name_enable" value="7" type="int" />
    <param name="button_name_home"  value="8" type="int" />

    <param name="button_preset_enable" value="7" type="int" />
    <param name="button_preset_no1" value="9" type="int" />
```

デフォルトのキー番号はこちらです。
![key_numbers](https://github.com/rt-net/crane_x7_ros/blob/images/images/joystick_example_key_numbers.png "key_numbers")

ジョイスティックのキー番号はトピック`/joy`で確認できます。

```sh
# ノードを起動する
roslaunch crane_x7_examples joystick_example.launch sim:=true

# 別のターミナルでコマンドを入力
rostopic echo /joy

# ジョイスティックのボタンを押す
header: 
  seq: 1
  stamp: 
    secs: 1549359364
    nsecs: 214800952
  frame_id: ''
axes: [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
buttons: [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
---
```

動作させると[こちら](https://youtu.be/IQci_vb3owM)のような動きになります。

---

### obstacle_avoidance_example.pyの実行

ROSのServiceを使って、障害物の追加と障害物回避をするコード例です。

次のコマンドでノードを起動します。

```sh
roslaunch crane_x7_examples obstacle_avoidance_example.launch
```

このサンプルでは目標姿勢と障害物の大きさ・姿勢を定義した[サービスファイル](./srv/ObstacleAvoidance.srv)を使用します。

目標姿勢と障害物の大きさ・姿勢は
[`crane_x7_examples/scripts/obstacle_client.py`](./scripts/obstacle_client.py)を編集することで変更できます。
デフォルトでは、直方体の箱を障害物として設定しています。

```python
    # 障害物を設定
    obstacle_name = "box"
    obstacle_size = Vector3(0.28, 0.16, 0.14)
    obstacle_pose_stamped = PoseStamped()
    obstacle_pose_stamped.header.frame_id = "/base_link"
    obstacle_pose_stamped.pose.position.x = 0.35
    obstacle_pose_stamped.pose.position.z = obstacle_size.z/2.0
```

安全のため障害物として床を設置しています。
不要であれば[`crane_x7_examples/scripts/obstacle_avoidance_example.py`](./scripts/obstacle_avoidance_example.py)
を編集してください。

```python
    # 安全のため床を障害物として生成する
    floor_name = "floor"
    floor_size = (2.0, 2.0, 0.01)
    floor_pose = PoseStamped()
    floor_pose.header.frame_id = "/base_link"
    floor_pose.pose.position.z = -floor_size[2]/2.0
    scene.add_box(floor_name, floor_pose, floor_size)
    rospy.sleep(SLEEP_TIME)
```

moveitが障害物回避のパスを生成できない場合、X7は動作せず、次の目標位置に対するパスを計算します。
この場合、サーバからの返答は`result=False`となります。

<img src="https://github.com/rt-net/crane_x7_ros/blob/images/images/obstacle_avoidance_1.png" width="400"><img src="https://github.com/rt-net/crane_x7_ros/blob/images/images/obstacle_avoidance_2.png" width="400">

---

### servo_info_example.pyの実行

サーボモータ（joint）の情報を取得するコード例です。

次のコマンドでノードを起動します。

```sh
rosrun crane_x7_examples servo_info_example.py
```

このサンプルではグリッパーのモータ`crane_x7_gripper_finger_a_joint`のトピックを取得しています。

実行するとターミナル画面にモータの電流・位置・温度が表示されます。

```sh
# 表示例
 current [mA]: 0.0     dxl_position: 2634    temp [deg C]: 42.0  
 current [mA]: 2.69    dxl_position: 2634    temp [deg C]: 42.0  
 current [mA]: 0.0     dxl_position: 2634    temp [deg C]: 42.0  
 current [mA]: 0.0     dxl_position: 2634    temp [deg C]: 42.0  
 current [mA]: 2.69    dxl_position: 2634    temp [deg C]: 42.0
 ...
```

また、電流が一定値を超えるとグリッパーを開く（閉じる）処理を入れてます。
これにより、手でグリッパーを開く（閉じる）ことができます。

トピックの詳細については、[`crane_x7_control/README.md`](../crane_x7_control/README.md#ネームスペースとトピック)を確認してください。

---

### pick_and_place_in_gazebo_example.pyの実行

![gazebo_pick_and_place](https://github.com/rt-net/crane_x7_ros/blob/images/images/gazebo_pick_and_place.png "gazebo_pick_and_place")

Gazebo上のモノを掴む・持ち上げる・運ぶ・置くコード例です。

gripperをEffortControllerで制御するため、オプションを追加してGazeboを起動します。

```sh
roslaunch crane_x7_gazebo crane_x7_with_table.launch use_effort_gripper:=true
```

Gazebo起動後、次のコマンドでサンプルを実行します。

```sh
rosrun crane_x7_examples pick_and_place_in_gazebo_example.py
```

動作させると[こちら](https://youtu.be/YUSIregHHnM)のような動きになります。

