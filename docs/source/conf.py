# -- Project information -----------------------------------------------------

project = 'courseutils'
copyright = '2026, Sarah M Brown'
author = 'Sarah M Brown '



# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    'sphinx.ext.intersphinx',
    "sphinx_design",
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_click'
]

# "sphinxext.rediraffe",

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', "*import_posts*",
        "**/pandoc_ipynb/inputs/*", ".nox/*", "README.md",]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pydata_sphinx_theme'


html_theme_options = {
  "show_nav_level": 2,
  "header_links_before_dropdown": 6,
  "icon_links": [ 
        {
            "name": "GitHub",
            "url": "https://github.com/compsys-progtools/courseutils",
            "icon": "fa-brands fa-github",
        },
        {
            "name": "Course",
            "url": "https://github.com/compsys-progtools/courseutils",
            "icon": "fa-solid fa-school",
        }],
  "secondary_sidebar_items": {
        "**/*": ["page-toc", "edit-this-page", "sourcelink"],
    }
}

# html_favicon = "_static/favicon.ico"
#  change this to change the site title
html_title = project

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
# html_extra_path = ["feed.xml"]
# map pages to which sidebar they should have
#  "page_file_name": ["list.html", "of.html", "sidebar.html", "files.html"]
html_sidebars = {
    "*": [],
    "**/*": ["sidebar-nav-bs",]
}

#     "about": ["hello.html"],
#     "publications": ["hello.html"],
#     "projects": ["hello.html"],
#     "resume": ["hello.html"],
#     "news": ["hello.html", 'archives.html'],
#     "news/**": ['postcard.html', 'recentposts.html', 'archives.html'],


# Panels config
panels_add_bootstrap_css = False

# MyST config
myst_enable_extensions = [
    # "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    # "linkify",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    # "tasklist",
]

# def setup(app):
#     app.add_css_file("custom.css")
