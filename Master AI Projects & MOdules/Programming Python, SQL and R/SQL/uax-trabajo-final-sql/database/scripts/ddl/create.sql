/* This script creates the tables for the universidad database */

CREATE TABLE IF NOT EXISTS departamento (
    id_departamento INTEGER NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS profesor (
    id_profesor INTEGER NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL,
    direccion TEXT,
    especialidad TEXT NOT NULL,
    id_departamento INTEGER NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES departamento(id_departamento)
);

CREATE TABLE IF NOT EXISTS estudiante (
    id_estudiante INTEGER NOT NULL PRIMARY KEY,
    nombre TEXT NOT NULL,
    direccion TEXT
);

CREATE TABLE IF NOT EXISTS asignatura (
    id_asignatura INTEGER NOT NULL PRIMARY KEY,
    titulo TEXT NOT NULL,
    creditos INTEGER NOT NULL,
    id_profesor INTEGER NOT NULL,
    FOREIGN KEY (id_profesor) REFERENCES profesor(id_profesor)
);

CREATE TABLE IF NOT EXISTS matricula (
    id_estudiante INTEGER NOT NULL,
    id_asignatura INTEGER NOT NULL,
    num_matricula INTEGER NOT NULL,
    fecha DATE NOT NULL,
    precio INTEGER NOT NULL,
    PRIMARY KEY (id_estudiante, id_asignatura, num_matricula),
    FOREIGN KEY (id_estudiante) REFERENCES estudiante(id_estudiante),
    FOREIGN KEY (id_asignatura) REFERENCES asignatura(id_asignatura)
);
