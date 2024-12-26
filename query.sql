create database DarwinCell

drop database DarwinCell

use DarwinCell


CREATE TABLE Productos (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(50) NOT NULL,
    modelo NVARCHAR(50) NOT NULL,
    especificaciones NVARCHAR(255),
    categoria NVARCHAR(20) NOT NULL,
    tipo_accesorio NVARCHAR(20),
    stock INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    imagen VARBINARY(MAX)
);

  
CREATE TABLE Clientes (
    id_cliente INT PRIMARY KEY IDENTITY,
    nombre NVARCHAR(100) NOT NULL,
    telefono NVARCHAR(15),
    email NVARCHAR(100)
);


CREATE TABLE Pedido (
    id_pedido INT PRIMARY KEY IDENTITY(1,1),
    codigo_pedido NVARCHAR(20) NOT NULL,     
    id_cliente INT,                           
    nombre_cliente NVARCHAR(100) NOT NULL,    
    id_producto INT NOT NULL,                
    cantidad INT NOT NULL,                    
    fecha_pedido DATETIME DEFAULT GETDATE(),  
    estado NVARCHAR(20) DEFAULT 'Pendiente',  
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),  
    FOREIGN KEY (id_producto) REFERENCES Productos(id)        
);

CREATE TABLE Factura (
    id_factura INT PRIMARY KEY IDENTITY(1,1),
    codigo_factura NVARCHAR(20) NOT NULL,
    codigo_pedido NVARCHAR(20) NOT NULL,
    id_cliente INT NOT NULL,
    nombre_cliente NVARCHAR(100),
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    fecha_factura DATETIME DEFAULT GETDATE(),
    fecha_pedido DATETIME NOT NULL,  -- Añadido campo para la fecha del pedido
    estado NVARCHAR(20) DEFAULT 'Completado',
    FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
    FOREIGN KEY (id_producto) REFERENCES Productos(id)
);


create table users(

    usr_id int PRIMARY key IDENTITY(1,1),
    usr_name NVARCHAR(20),
    usr_password NVARCHAR(15),
    usr_privileg NVARCHAR(10)
)


create Table db_admin(
    db_id INT IDENTITY(1,1) PRIMARY KEY,
    db_user NVARCHAR(12),
    db_password  VARCHAR(10)
)

insert into db_admin (db_user, db_password) values ('Miguel', 'AdminDb54' )


SELECT * FROM Productos
