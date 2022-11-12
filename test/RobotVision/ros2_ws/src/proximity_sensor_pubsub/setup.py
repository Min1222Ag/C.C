from setuptools import setup

package_name = 'proximity_sensor_pubsub'

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
    description='Using a proximity sensor it can get distance',
    license='TeamC.C',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            "proximity_detect_node = proximity_sensor_pubsub.proximity_detect_node:main" 
        ],
    },
)
