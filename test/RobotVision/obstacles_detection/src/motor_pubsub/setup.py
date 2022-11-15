from setuptools import setup

package_name = 'motor_pubsub'

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
    maintainer='pi',
    maintainer_email='yhb1834@hanmail.net',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motor_node = motor_pubsub.motor_node:main',
            'talker = motor_pubsub.motor_publisher:main',
            'listener = motor_pubsub.motor_subscriber:main',
        ],
    },
)
