"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure



app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    firstname = Column(String(100), nullable=True)
    lastname = Column(String(100), nullable=True)
    fecha_subscripcion = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
   
    favoritos_personajes = relationship("FavoritoPersonaje", back_populates="usuario")
    favoritos_planetas = relationship("FavoritoPlaneta", back_populates="usuario")
    posts = relationship("Post", back_populates="autor")
    comentarios = relationship("Comentario", back_populates="autor")

class Personaje(Base):
    __tablename__ = 'personaje'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    altura = Column(String(20), nullable=True)
    peso = Column(String(20), nullable=True)
    color_cabello = Column(String(50), nullable=True)
    color_piel = Column(String(50), nullable=True)
    color_ojos = Column(String(50), nullable=True)
    ano_nacimiento = Column(String(20), nullable=True)
    genero = Column(String(20), nullable=True)
    planeta_origen_id = Column(Integer, ForeignKey('planeta.id'), nullable=True)
    descripcion = Column(Text, nullable=True)
    
    
    planeta_origen = relationship("Planeta", back_populates="personajes_nativos")
    favoritos = relationship("FavoritoPersonaje", back_populates="personaje")

class Planeta(Base):
    __tablename__ = 'planeta'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    periodo_rotacion = Column(String(20), nullable=True)
    periodo_orbital = Column(String(20), nullable=True)
    diametro = Column(String(20), nullable=True)
    clima = Column(String(100), nullable=True)
    gravedad = Column(String(20), nullable=True)
    terreno = Column(String(100), nullable=True)
    agua_superficial = Column(String(20), nullable=True)
    poblacion = Column(String(50), nullable=True)
    descripcion = Column(Text, nullable=True)
    
   
    personajes_nativos = relationship("Personaje", back_populates="planeta_origen")
    favoritos = relationship("FavoritoPlaneta", back_populates="planeta")

class FavoritoPersonaje(Base):
    __tablename__ = 'favorito_personaje'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    personaje_id = Column(Integer, ForeignKey('personaje.id'), nullable=False)
    fecha_agregado = Column(DateTime, default=datetime.utcnow)
    
   
    usuario = relationship("Usuario", back_populates="favoritos_personajes")
    personaje = relationship("Personaje", back_populates="favoritos")

class FavoritoPlaneta(Base):
    __tablename__ = 'favorito_planeta'
    
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    planeta_id = Column(Integer, ForeignKey('planeta.id'), nullable=False)
    fecha_agregado = Column(DateTime, default=datetime.utcnow)
    
   
    usuario = relationship("Usuario", back_populates="favoritos_planetas")
    planeta = relationship("Planeta", back_populates="favoritos")

class Post(Base):
    __tablename__ = 'post'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    autor_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    is_published = Column(Boolean, default=True)
    
   
    autor = relationship("Usuario", back_populates="posts")
    comentarios = relationship("Comentario", back_populates="post")

class Comentario(Base):
    __tablename__ = 'comentario'
    
    id = Column(Integer, primary_key=True)
    contenido = Column(Text, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    autor_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    
 
    autor = relationship("Usuario", back_populates="comentarios")
    post = relationship("Post", back_populates="comentarios")


def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}


Usuario.to_dict = to_dict
Personaje.to_dict = to_dict
Planeta.to_dict = to_dict
FavoritoPersonaje.to_dict = to_dict
FavoritoPlaneta.to_dict = to_dict
Post.to_dict = to_dict
Comentario.to_dict = to_dict