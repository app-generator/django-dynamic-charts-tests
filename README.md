# Dynamic charts for Django

The project needs to provide a way to chart data using a minimal inoput from the user. Library will manages the charts in two ways:

The input is basically any Model defined in any application. For initial tests, we will use one defined a simple `Sales` model:

```python
class Sales(models.Model):
    id            = models.AutoField(primary_key=True)
    product       = models.CharField(max_length = 100) # name: Nike AIR, PUMA 
    price         = models.IntegerField()              # 99
    fee           = models.IntegerField()              # 5
    currency      = models.CharField(max_length = 3)   # usd, eur, chn
    country       = models.CharField(max_length = 100) # usa, ch, ro
    purchase_date = models.IntegerField()              # Unix Timestamp 
```

The information is extracted using Charts.JS (CDN import) and presented to the user in two ways: 

<br />

> 👉 **(1)** Via a route 

The syntax is this: `localhost:8000/dyn-chart/MODEL/CHART_TYPE/COL_1/COL_2/COL3/`

- 1.1 **PIE Chart**: `localhost:8000/dyn-chart/sales/pie/country/report_start/`
  - INPUTS (for PIE) 
    - COL_1: mandatory
    - COL_2: optional: number of days to report: 10, 20, 
      - if not provided or negative, the report use ALL time data 
  - Samples:
    - `localhost:8000/dyn-chart/sales/pie/country/20/` - PIE chart for Country sales, in the last 20 days
    - `localhost:8000/dyn-chart/sales/pie/country/` - PIE chart for Country sales, ALL time report 
    - `localhost:8000/dyn-chart/sales/pie/currency/5/` - PIE chart for Currencies in the last 5 days 
    
<br />

> 👉 **(2)** Widget Mode 

@Todo 

<br />

---

<br />

## Start the app in Docker

> 👉 **Step 1** - Download the code from the GH repository (using `GIT`)

```bash
$ git clone https://github.com/app-generator/django-adminlte.git
$ cd django-adminlte
```

> 👉 **Step 2** - Start the APP in `Docker`

```bash
$ docker-compose up --build
```

Visit `http://localhost:5085` in your browser. The app should be up & running.

<br />

## Manual Build 

> 👉 Download the code  

```bash
$ git clone https://github.com/app-generator/django-adminlte.git
$ cd django-adminlte
```

<br />

> 👉 Install modules via `VENV`  

```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

<br />

> 👉 Set Up Database

```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

<br />

> 👉 Create the Superuser

```bash
$ python manage.py createsuperuser
```

<br />

> 👉 Start the app

```bash
$ python manage.py runserver
```

At this point, the app runs at `http://127.0.0.1:8000/`. 

<br />

## Codebase structure

The project is coded using a simple and intuitive structure presented below:

```bash
< PROJECT ROOT >
   |
   |-- core/                            
   |    |-- settings.py                  # Project Configuration  
   |    |-- urls.py                      # Project Routing
   |
   |-- home/
   |    |-- views.py                     # APP Views 
   |    |-- urls.py                      # APP Routing
   |    |-- models.py                    # APP Models 
   |    |-- tests.py                     # Tests  
   |    |-- templates/                   # Theme Customisation 
   |         |-- includes                # 
   |              |-- custom-footer.py   # Custom Footer      
   |     
   |-- requirements.txt                  # Project Dependencies
   |
   |-- env.sample                        # ENV Configuration (default values)
   |-- manage.py                         # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />

## How to Customize 

When a template file is loaded, `Django` scans all template directories starting from the ones defined by the user, and returns the first match or an error in case the template is not found. 
The theme used to style this starter provides the following files: 

```bash
# This exists in ENV: LIB/admin_adminlte
< UI_LIBRARY_ROOT >                      
   |
   |-- templates/                     # Root Templates Folder 
   |    |          
   |    |-- accounts/       
   |    |    |-- login.html           # Sign IN Page
   |    |    |-- register.html        # Sign UP Page
   |    |
   |    |-- includes/       
   |    |    |-- footer.html          # Footer component
   |    |    |-- sidebar.html         # Sidebar component
   |    |    |-- navigation.html      # Navigation Bar
   |    |    |-- scripts.html         # Scripts Component
   |    |
   |    |-- layouts/       
   |    |    |-- base.html            # Masterpage
   |    |    |-- base-auth.html       # Masterpage for Auth Pages
   |    |
   |    |-- pages/       
   |         |-- index.html           # Dashboard Page
   |         |-- calendar.html        # Profile Page
   |         |-- *.html               # All other pages
   |    
   |-- ************************************************************************
```

When the project requires customization, we need to copy the original file that needs an update (from the virtual environment) and place it in the template folder using the same path. 

> For instance, if we want to **customize the footer.html** these are the steps:

- ✅ `Step 1`: create the `templates` DIRECTORY inside the `home` app
- ✅ `Step 2`: configure the project to use this new template directory
  - `core/settings.py` TEMPLATES section
- ✅ `Step 3`: copy the `footer.html` from the original location (inside your ENV) and save it to the `home/templates` DIR
  - Source PATH: `<YOUR_ENV>/LIB/admin_adminlte/template/includes/footer.html`
  - Destination PATH: `<PROJECT_ROOT>home/templates/includes/footer.html`

> To speed up all these steps, the **codebase is already configured** (`Steps 1, and 2`) and a `custom footer` can be found at this location:

`home/templates/includes/custom_footer.html` 

By default, this file is unused because the `theme` expects `footer.html` (without the `custom-` prefix). 

In order to use it, simply rename it to `footer.html`. Like this, the default version shipped in the library is ignored by Django. 

In a similar way, all other files and components can be customized easily.

<br />

## Deploy on [Render](https://render.com/)

- Create a Blueprint instance
  - Go to https://dashboard.render.com/blueprints this link.
- Click `New Blueprint Instance` button.
- Connect your `repo` which you want to deploy.
- Fill the `Service Group Name` and click on `Update Existing Resources` button.
- After that your deployment will start automatically.

At this point, the product should be LIVE.

<br />

## [PRO Version](https://appseed.us/product/material-dashboard2-pro/django/)   

This design is a pixel-perfect [Bootstrap 5](https://www.admin-dashboards.com/bootstrap-5-templates/) Dashboard with a fresh, new design inspired by Google's Material Design. `Material Dashboard 2 PRO` is built with over 300 frontend individual elements, like buttons, inputs, navbars, nav tabs, cards, or alerts, giving you the freedom of choosing and combining.

> Features: 

- ✅ `Up-to-date Dependencies`
- ✅ `Design`: [Django Theme Material2](https://github.com/app-generator/django-admin-material2-pro) - `PRO Version`
- ✅ `Sections` covered by the design:
  - ✅ **Admin section** (reserved for superusers)
  - ✅ **Authentication**: `Django.contrib.AUTH`, Registration
  - ✅ **All Pages** available in for ordinary users 
- ✅ `Docker`
- 🚀 `Deployment` 
  - `CI/CD` flow via `Render`

<br />

![Material Dashboard 2 Pro](https://user-images.githubusercontent.com/51070104/211141418-6b7886eb-6fb3-433e-91c9-2895c086099a.png)

<br />

---
[Django AdminLTE](https://appseed.us/product/adminlte/django/) - Open-Source **Django** starter provided by **[AppSeed](https://appseed.us/)**
