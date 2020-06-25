#project is folder (package) name inside which forms.py is present
import zipfile
import os
from flask import send_file
from flask import Flask, request, abort, jsonify, send_from_directory
from flask import render_template, url_for, flash, redirect, render_template_string
from project.forms import Edit,Delete,Upload
from project import app
from .makehtml import *
from .update_db import *
import pandas as pd
import numpy as np
import random,os
from werkzeug.utils import secure_filename

accessCode='1234'
    
@app.route("/")
@app.route("/home")
def home():
    data=readData()
    print("data fetched")
    table=makeTable(data)    
    mapped_table,releases,ver_map=mapTable(table)
    ver_map=assignColorNumber(ver_map)
    colors=colorMap(ver_map)
    black_list=getBlackList(readBlackListDB())
    css=makeCSS(colors)
    html=makeHTMLtable(mapped_table,ver_map,black_list,css)
    print("webpage sent")
    if 'DataBases.zip' in os.listdir(os.getcwd()):
        os.remove('DataBases.zip')    
    return render_template_string(html)



@app.route("/edit", methods=['GET', 'POST'])
def edit():
    print("Main edit attempt")
    form = Edit()        
    if form.validate_on_submit():
        data=readFlaskDB()
        block=form.information_block.data
        value=form.attribute.data   
        des=form.description.data     
        if form.access.data != accessCode:
            flash('Wrong Access Code !!  Please retry', 'danger')
        elif check(block,value,data)== True:
            data=updateDescription(block,value,des,data)
            updateFlaskDB(data)
            flash(' Description Updated ! Please refresh the page.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Description not updated ( Invalid Information Block / Attribute ), Please retry ', 'danger')
    return render_template('edit.html', title='Edit', form=form)

@app.route("/delete", methods=['GET', 'POST'])
def delete():
    print("delete attempt")
    form = Delete()    
    if form.validate_on_submit():
        data=readFlaskDB()
        block=form.information_block.data
        value=form.attribute.data
        if form.access.data != accessCode:
            flash('Wrong Access Code !!  Please retry', 'danger')
        elif check(block,value,data) == True:
            new_block,new_value=getBlockValue(block,value,data)
            blacklist_db = readBlackListDB()
            updateBlackListDB(blacklist_db,new_value)
            flash(' Attribute Removed ! Please refresh the page.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Attribute Not Deleted ( Invalid Information Block / Attribute ), Please retry ', 'danger')
    return render_template('delete.html', title='Delete', form=form)


@app.route('/download_all')
def download_all():
    zipf = zipfile.ZipFile('DataBases.zip','w', zipfile.ZIP_DEFLATED)
    directory=os.getcwd()
    for file in os.listdir(directory):
        if ".csv" in file:
            zipf.write(file)        
    zipf.close()
    return send_from_directory(directory,'DataBases.zip', as_attachment=True)

ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validateDb(dbtype):
    data = pd.read_csv("validate.csv")
    col = data.columns
    boolean = True
    if dbtype =="flaskdb":
        if len(col)!= 4:
            boolean = False
            return boolean
        if col[0]!='Information Block' or col[1]!='Attribute' or col[2] !='ISE Version' or col[3] != 'Description':
            boolean = False
            return boolean
    else:
        if len(col) != 1:
            boolean = False
            return boolean
        if col[0]!= 'Blacklisted':
            boolean = False
            return boolean
    return boolean
        


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    form = Upload()
    if request.method == "POST" and form.validate_on_submit():
        if form.access.data != accessCode:
            flash('Wrong Access Code !!  Please retry', 'danger')    
        elif request.files:
            file = request.files["file"]
            print("File recieved")
            print(file.filename)
            filename = secure_filename(file.filename)
            if allowed_file(filename)==False:
                flash('Wrong File Type (only .csv is accepted) !!  Please retry', 'danger')                
            else:
                dbtype=str(form.dbtype.data)
                file.filename="validate.csv"
                filename=file.filename
                file.save(os.path.join(os.getcwd(),filename))
                if validateDb(dbtype):
                    updateNewDB(dbtype)
                    if 'validate.csv' in os.listdir(os.getcwd()):
                        os.remove('validate.csv')
                    print("File Saved")
                    flash(' Database Updated !!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Wrong Database Format !!  Please check Database and retry', 'danger')
    return render_template("upload.html",form=form)

@app.route("/try", methods=['GET', 'POST'])
def newedit():
    print("mini edit attempt")
    form = Edit()
    if request.method == "POST":
        info=request.form['information']
        info=info.split()
        form.information_block.data=info[0]
        form.attribute.data=info[1]
    return render_template('edit.html', title='Edit',form=form)

@app.route("/hide", methods=['GET', 'POST'])
def newhide():
    print("mini Hide attempt")
    form = Delete()
    if request.method == "POST":
        info=request.form['information']
        info=info.split()
        form.information_block.data=info[0]
        form.attribute.data=info[1]
    return render_template('delete.html', title='Hide',form=form)
