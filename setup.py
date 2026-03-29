from setuptools import find_packages, setup

package_name = 'diff_to_acker'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/systemd',
        ['systemd/diff_to_acker.service']),
    ('share/' + package_name + '/scripts',
        ['scripts/install_service.sh']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='victor.dubois@outlook.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'converter_node = diff_to_acker.converter_node:main',
        ],
    },
)
