import click
import json
import yaml
import os
import subprocess
from datetime import date
import requests

from .config import GH_APPROVERS, BASE_URL


@click.group()
def csssem_util():
    pass
# --------------------------------------------------------------
#          Manage Assignments
# --------------------------------------------------------------


assignment_paths = {'Prepare (Basic)': 'prepare/basic.md',
'Prepare (Advanced)': 'prepare/advanced.md',
'Exit Ticket': 'reflect/exit.md',
'Talk Reflection': 'reflect/debreif.md',}

banch_names = {'Prepare (Basic)': 'prepare',
'Prepare (Advanced)': 'prepare',
'Exit Ticket': 'reflect',
'Talk Reflection': 'reflect',}

template_types = assignment_paths.keys()


@csssem_util.command()
@click.option('-t', '--type', default='prepare',
                help='type can be ' + ', '.join(template_types) , 
                required=True)
@click.option('-d','--date', default=None, required=True,
                help='date should be YYYY-MM-DD of the relevant seminar')
@click.option('--out_path', default=None, required=False,
                help='path to save the file; default current directory')    
def gettemplatefile(type,date,out_path):
    '''
    get template file for activity from the course website repo
    '''
    #  build file url from base and type 
    relative_path = assignment_paths.get(type)
    file_url = f"{BASE_URL}/{relative_path}"
    # load file from base url
    click.echo(file_url)
    template_content = requests.get(file_url).text

    if not(out_path):
        out_path = relative_path.replace('.','_'+date+'.')

    with open(out_path,'w') as f:
        f.write(template_content)

@csssem_util.command()
@click.argument('type', type=click.Choice(template_types))

def acbranch(type):
    '''
    create assignment branch and PR for the given type and date
    '''
    click.echo(banch_names.get(type))
