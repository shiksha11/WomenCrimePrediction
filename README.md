# WomenCrimePrediction

### Motivation Behind The Project
India is the most dangerous country for women owing to high rate of sexual violence, lack of access to justice in rape cases and human trafficking. 
Several factors can influence the crime rates at any location like demographic features including literacy rate, gender distribution, population density among others. 
Thus we are making an attempt to predict the probability of different types of crime in a locality by augmenting the First Information Report (FIR) 
prepared by the police stations with its demographic data. These probability predictions can be used to warn women if they are about to enter 
any unsafe area.

### Installation Guide
1. If python is not already installed in your system, first of all install python -  [link](https://www.python.org/downloads/) 
2. Similarly, if git is not currently install, install git to clone the project - [link](https://git-scm.com/downloads)
3. Now, open command promt or terminal and move to the folder where you want to clone the project.
4. Initialize virtual environment(say django_env) using 
   * python -m venv django_env
6. Activate virtual enviroment using 
   * source django_env/bin/activate(mac)
   * C:\> <venv>\Scripts\activate.bat (windows)
7. Now, move into the django_env folder
8. Clone the project using - 
   * git clone "https://github.com/shiksha11/WomenCrimePrediction.git"
9. Move into the projects folder using -
   * cd blogs
10. Setup project using - 
   * pip intall -r requirements.txt
11. Host the project locally using - 
   * python manage.py runserver
12. Copy and paste the address in any web browser to explore the web-app :)


### Future Scope 
1. The project is currently only restricted to one state in India. In future, with similar approach it can be extended to any states or country if
we have data available for it. 
