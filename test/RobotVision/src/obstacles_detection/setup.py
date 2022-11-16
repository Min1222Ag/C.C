from setuptools import setup

package_name = 'obstacles_detection'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='teamc.c2022',
    maintainer_email='teamc.c2022@gmail.com',
    description='For obstacles detection using LiDAR, camera, and proximity sensor',
    license='TEAM C.C',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = obstacles_detection.obstacles_detect_node:main'
        ],
    },
)
