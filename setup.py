from setuptools import setup

requires = [
    'PyPDF2',
    'pdftotext',
]

setup(
    name="MagicalQuill",
    version="0.2.2",
    description="Outil pour traiter les dossiers PDF des candidats ParcourSup.",
    url="https://github.com/Epithumia/MagicalQuill",
    packages=['magicalquill'],
    install_requires=requires,
    scripts=['magicalquill/shell/process.sh'],
    entry_points={
        'console_scripts': ['decoupe-psup=magicalquill.magicalquill:main'],
    }
)
