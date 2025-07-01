from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Node(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer)
    scenario = db.Column(db.String(200))
    parent_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    best_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    realistic_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    worst_id = db.Column(db.Integer, db.ForeignKey('node.id'))
    best = db.relationship('Node', remote_side=[id], foreign_keys=[best_id])
    realistic = db.relationship('Node', remote_side=[id], foreign_keys=[realistic_id])
    worst = db.relationship('Node', remote_side=[id], foreign_keys=[worst_id])
 
