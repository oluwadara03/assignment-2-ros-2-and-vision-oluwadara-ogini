from setuptools import find_packages, setup

# The package name
package_name = 'aisd_vision'

setup(
	# Package metadata
    name=package_name,
    version='0.0.0',
	
	# Find all packages, but excluding test packages
    packages=find_packages(exclude=['test']),
    data_files=[
		# Registers package so ROS 2 tools can find it
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
	
	# Required Python dependencies
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aisd',
    maintainer_email='93853037+oluwadara03@users.noreply.github.com',
    description='ROS2 vision setup',
    license='no license',

	# Testing dependencies (optional)
    extras_require={
        'test': [
            'pytest',
        ],
    },

	# ROS 2 nodes mapped to Python functions
    entry_points={
        'console_scripts': [
	    'image_publisher = aisd_vision.image_publisher:main',
 	    'hands = aisd_vision.hands:main',
        ],
    },
)
