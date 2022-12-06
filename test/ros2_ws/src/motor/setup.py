from setuptools import setup

package_name = 'motor'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='c.c',
    maintainer_email='c.c@gmail.com',
    description='Control Overall Driving throught the motors',
    license='Apache 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'talker = motor.publisher_motor_function:main',    # publish the information about motor, but not be used now
            'listener = motor.subscriber_motor_function:main',  # activate subscription from obstacles_detect_node 
        ],
    },
)
