import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch_ros.actions import PushRosNamespace

def generate_launch_description():
    # パッケージ名とXMLファイル名を指定
    package_name = 'astra_camera'
    launch_file_name = 'astra_pro.launch.xml'

    # XMLファイルのパスを取得
    xml_launch_path = os.path.join(
        get_package_share_directory(package_name),
        'launch',
        launch_file_name
    )

    # --- カメラ1の設定 ---
    # 手順1で調べた「シリアル番号」を入力してください
    camera1_serial = '18081530273' 
    
    camera1_node = GroupAction(
        actions=[
            PushRosNamespace('camera1'), # 名前空間を分ける (/camera1/...)
            IncludeLaunchDescription(
                AnyLaunchDescriptionSource(xml_launch_path),
                launch_arguments={
                    'serial_number': camera1_serial, # 手順1で確認した引数名に合わせる
                    'camera_name': 'camera1'         # TFなどが重複しないように名前を変更
                }.items()
            )
        ]
    )

    # --- カメラ2の設定 ---
    # もう1台の「シリアル番号」を入力してください
    camera2_serial = '19052230002'

    camera2_node = GroupAction(
        actions=[
            PushRosNamespace('camera2'), # 名前空間を分ける (/camera2/...)
            IncludeLaunchDescription(
                AnyLaunchDescriptionSource(xml_launch_path),
                launch_arguments={
                    'serial_number': camera2_serial,
                    'camera_name': 'camera2'
                }.items()
            )
        ]
    )

    return LaunchDescription([
        camera1_node,
        camera2_node
    ])