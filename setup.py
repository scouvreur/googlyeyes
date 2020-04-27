import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="googleyeyes", # Replace with your own username
    version="0.0.1",
    author="Stephane Couvreur",
    author_email="stephane.couvreur.sueron@gmail.com",
    description="A lightweight web application which adds googly eyes to an image sent to its POST endpoint",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scouvreur/googlyeyes",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
