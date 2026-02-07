import click
import json
import yaml
import os
import subprocess
from datetime import date
import requests
import pandas as pd

from .config import GH_APPROVERS, BASE_URL


@click.group()
def csssem_util():
    pass
# --------------------------------------------------------------
#          Manage Assignments
# --------------------------------------------------------------


assignment_paths = {'Prepare (Basic)': 'prepare/basic.md',
'Prepare (Advanced)': 'prepare/advanced.md',
'Exit Ticket': 'reflection/exit.md',
'Talk Reflection': 'reflection/debreif.md',}

banch_names = {'Prepare (Basic)': 'prepare',
'Prepare (Advanced)': 'prepare',
'Exit Ticket': 'reflect',
'Talk Reflection': 'reflect',}

template_types = assignment_paths.keys()


all_date_list = ['2026-01-30', '2026-02-06', '2026-02-13', '2026-02-20', '2026-02-27', '2026-03-06', '2026-03-13', '2026-03-27', '2026-04-03', '2026-04-10', '2026-04-17', '2026-04-24']


@csssem_util.command()
@click.option('-t', '--type', type=click.Choice(template_types), required=True,
                help='type can be ' + ', '.join(template_types) , 
                prompt=True, show_choices=True)
@click.option('-d','--date',  required=True, type=click.Choice(all_date_list), prompt=True, show_choices=True,
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


grade_files = ['attendance','prepare','reflect']
@csssem_util.command()
@click.argument('type', type=click.Choice(grade_files)) 
@click.argument('rating') 
def eval(type,event, rating):
    '''
    evaluate submissions for the given date and type
    '''
    file_name = type + '.csv'
    with open(file_name,'a') as f:
        f.write(f"{event},{rating}\n")


summary_tamplate = '''
# Grade Summary


This will be automatically updated periodically.  When it is updated, it will include a timestamp. 

Any work done after that timestamp will not be reflected. 


You cannot edit the files in this folder. The csvs are where the instructor records evaluations. 

## Preparation

Your current prepararation ratings are below. You need at least 12 attempted or complete and at least 10 complete. 

{calc_prep}

## Attendance

You need to earn 10 present, active or excused ratings to pass. 
{calc_attendance}

## Reflection

You need to earn 24 units of reflction and synthesis to pass.  

SO far you have earned {calc_reflect} units
'''

@csssem_util.command()

def calculateprogress():
    '''
    calculate progress for  student based on graded items
    '''
    df_prep = pd.read_csv('.grades/preparation.csv')
    df_attendance = pd.read_csv('.grades/attendance.csv')

    calc_prep = df_prep['rating'].value_counts().to_markdown()
    calc_attendance = df_attendance['rating'].value_counts().to_markdown()

    df_reflect = pd.read_csv('.grades/reflection.csv')
    calc_reflect = df_reflect['units'].sum()

    click.echo(summary_tamplate.format(calc_prep=calc_prep, calc_attendance=calc_attendance, calc_reflect=calc_reflect))


index_col = {'attendance': 'date', 'prepare': 'date', 'reflection': 'activity'}
@csssem_util.command()
@click.argument('type', type=click.Choice(grade_files))

def resolveevals(type):
    '''
    resolve evaluations for a given file and return a summary
    '''
    filename = type + '.csv'
    path = os.path.join('.grades',filename)
    with open(path,'r') as f:
        lines = f.readlines()
    
    # drop merge conflict lines
    lines = [l for l in lines if not l.startswith('<<<<<<<') and not l.startswith('=======') and not l.startswith('>>>>>>>')]
    # parse csv
    with open(path,'w') as f:
        f.writelines(lines)

    df = pd.read_csv(path,index_col=index_col.get(type))
    if df.index.has_duplicates:
        click.echo(f"Warning: there are duplicate entries for {type} evaluations. Please resolve manually.")
    


def updateaction():
    '''
    update list of dates available based on graded items
    '''
    df_prep = pd.read_csv('preparation.csv')
    df_reflect = pd.read_csv('reflection.csv')
    #  get dates from graded items

    # if a date appears in both refelect and prepare, remove it
    # for date in all_date_list:
        
