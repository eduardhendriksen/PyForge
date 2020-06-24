from distutils.core import setup
setup(
  name = 'pyforge',
  packages = ['pyforge'],
  version = '0.2',
  license='MIT',
  description = 'Python tools to communicate with the Autodesk Forge Api.',
  author = 'Eduard Hendriksen',
  author_email = 'e.c.hendriksen@gmail.com',
  url = 'https://github.com/eduardhendriksen/PyForge',
  download_url = 'https://github.com/eduardhendriksen/PyForge/archive/master.tar.gz',
  keywords = ['Autodesk Forge', 'API'],
  install_requires=['requests'],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
	  'Programming Language :: Python :: 3.7',
	  'Programming Language :: Python :: 3.8'
  ],
)