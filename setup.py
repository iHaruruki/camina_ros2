from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'camina_ros2'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*launch.[pxy][yma]*')),
        (os.path.join('share', package_name, 'rviz'),   glob('rviz/*.rviz')),
        (os.path.join('share', package_name), glob('urdf/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='HarukiIsono',
    maintainer_email='haruki.isono861@gmail.com',
    description='This is camina repository',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'front_ramera_node = camina_ros2.front_camera:main',
            'rear_camera_node = camina_ros2.rear_camera:main',
        ],
    },
)
