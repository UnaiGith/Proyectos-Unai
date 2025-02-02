/* This script inserts data into the tables of the pedido database */


/* Delete all the previous data from the tables */

DELETE FROM profesor;
DELETE FROM departamento;
DELETE FROM matricula;
DELETE FROM asignatura;
DELETE FROM estudiante;


/* Insert departments */

INSERT INTO departamento (id_departamento, nombre) VALUES (1, 'Ingenieria');
INSERT INTO departamento (id_departamento, nombre) VALUES (2, 'Matematicas');
INSERT INTO departamento (id_departamento, nombre) VALUES (3, 'Literatura');
INSERT INTO departamento (id_departamento, nombre) VALUES (4, 'Historia');
INSERT INTO departamento (id_departamento, nombre) VALUES (5, 'Economia');
INSERT INTO departamento (id_departamento, nombre) VALUES (6, 'Biologia');
INSERT INTO departamento (id_departamento, nombre) VALUES (7, 'Fisica');


/* Insert teachers */

INSERT INTO profesor (id_profesor, nombre, direccion, especialidad, id_departamento)
VALUES (1, 'Carlos', 'Av. Las Fuentes', 'Programacion', 1);
INSERT INTO profesor (id_profesor, nombre, direccion, especialidad, id_departamento)
VALUES (2, 'Marta', 'Calle Mayor', 'Algebra', 2);
INSERT INTO profesor (id_profesor, nombre, direccion, especialidad, id_departamento)
VALUES (3, 'Sofia', 'Ctra. Principal', 'Escritura creativa', 3);
INSERT INTO profesor (id_profesor, nombre, direccion, especialidad, id_departamento)
VALUES (4, 'Pablo', 'Avenida del Parque', 'Historia Contemporanea', 4);
INSERT INTO profesor (id_profesor, nombre, direccion, especialidad, id_departamento)
VALUES (5, 'Laura', 'Calle del Triunfo', 'Microeconomia', 5);
INSERT INTO profesor (id_profesor, nombre, direccion, especialidad, id_departamento)
VALUES (6, 'Irene', NULL, 'Genetica', 6);                                             /* a teacher without address */
INSERT INTO profesor (id_profesor, nombre, direccion, especialidad, id_departamento)
VALUES (7, 'German', NULL, 'Mecanica Clasica', 7);                                    /* a teacher without address */
INSERT INTO profesor (id_profesor, nombre, direccion, especialidad, id_departamento)
VALUES (8, 'Elena', 'Calle Esperanza', 'Sistemas Distribuidos', 1);
INSERT INTO profesor (id_profesor, nombre, direccion, especialidad, id_departamento)
VALUES (9, 'Miguel', 'Calle Luna', 'Estadistica', 2);
INSERT INTO profesor (id_profesor, nombre, direccion, especialidad, id_departamento)
VALUES (10, 'Teresa', 'Calle del Sol', 'Poesia Barroca', 3);                          /* a teacher without subject */
INSERT INTO profesor (id_profesor, nombre, direccion, especialidad, id_departamento)
VALUES (11, 'Diego', 'Avenida Universidad', 'Calculo Avanzado', 2);                   /* a teacher without subject */
INSERT INTO profesor (id_profesor, nombre, direccion, especialidad, id_departamento)
VALUES (12, 'Beatriz', 'Calle Manantial', 'Robotica', 1);                             /* a teacher without subject */


/* Insert students */

INSERT INTO estudiante (id_estudiante, nombre, direccion)
VALUES (1, 'Luis', 'Gran Via');
INSERT INTO estudiante (id_estudiante, nombre, direccion)
VALUES (2, 'Ana', 'Calle Real');
INSERT INTO estudiante (id_estudiante, nombre, direccion)
VALUES (3, 'Lucia', 'Plaza Victoria');
INSERT INTO estudiante (id_estudiante, nombre, direccion)
VALUES (4, 'Mario', 'Calle Aragon');
INSERT INTO estudiante (id_estudiante, nombre, direccion)
VALUES (5, 'Patricia', 'Av. Del Este');
INSERT INTO estudiante (id_estudiante, nombre, direccion)
VALUES (6, 'Roberto', 'Plaza del Mar');
INSERT INTO estudiante (id_estudiante, nombre, direccion)
VALUES (7, 'Carmen', 'Calle la Paz');                      /* a student without enrollments */
INSERT INTO estudiante (id_estudiante, nombre, direccion)
VALUES (8, 'Sara', 'Calle Principal');                     /* a student without enrollments */
INSERT INTO estudiante (id_estudiante, nombre, direccion)
VALUES (9, 'David', NULL);                                 /* a student without address */
INSERT INTO estudiante (id_estudiante, nombre, direccion)
VALUES (10, 'Paula', NULL);                                /* a student without address */


/* Insert subjects */

INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (1, 'Fundamentos de Programacion', 6, 1);
INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (2, 'Calculo I', 6, 2);
INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (3, 'Literatura Medieval', 6, 3);
INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (4, 'Historia Moderna', 6, 4);
INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (5, 'Macroeconomia', 12, 5);
INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (6, 'Biologia Celular', 6, 6);
INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (7, 'Fisica Avanzada', 12, 7);
INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (8, 'Introducción a Sistemas Distribuidos', 6, 8);
INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (9, 'Análisis Avanzado de Estadística', 12, 9);
INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (10, 'Estructuras de Datos', 6, 1);                             /* teacher 1 has more than one subject */
INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (11, 'Algoritmos Avanzados', 6, 1);                             /* teacher 1 has more than one subject */
INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (12, 'Álgebra Lineal', 6, 2);                                   /* teacher 2 has more than one subject */
INSERT INTO asignatura (id_asignatura, titulo, creditos, id_profesor)
VALUES (13, 'Taller de Escritura', 6, 3);                              /* teacher 3 has more than one subject */


/* Insert enrollments */

/* all subjects require at least one enrollment */
/* subjects with 6 credits cost 100 for the first enrollment, 200 for the second, and 300 for the third */
/* subjects with 12 credits cost 200 for the first enrollment, 400 for the second, and 600 for the third */

/* student 1 */
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (1, 1, 1, '2020-09-01', 100);
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (1, 2, 1, '2020-09-01', 100);
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (1, 8, 1, '2020-09-01', 100);
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (1, 10, 2, '2020-09-01', 200);                                               /* student 1 has failed this subject once, so this is the second enrollment, and the price is 200 */
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (1, 12, 3, '2020-09-01', 300);                                               /* student 1 has failed this subject twice, so this is the third enrollment, and the price is 300 */
/* student 2 */
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (2, 3, 1, '2020-09-02', 100);
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (2, 13, 1, '2020-09-02', 100);
/* student 3 */
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (3, 1, 1, '2020-09-03', 100);
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (3, 9, 3, '2020-09-03', 600);                                                /* student 3 has failed this subject twice, so this is the third enrollment, and the price is 600, because the subject has 12 credits */
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (3, 11, 1, '2020-09-03', 100);
/* student 4 */
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (4, 3, 1, '2020-09-04', 100);
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (4, 4, 1, '2020-09-05', 100);
/* student 5 */
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (5, 5, 1, '2020-09-04', 200);
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (5, 9, 1, '2020-09-06', 200);
/* student 6 */
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (6, 6, 1, '2020-09-05', 100);
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (6, 9, 1, '2020-09-05', 200);
/* students 7 and 8 have no enrollments */
/* student 9 */
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (9, 7, 1, '2020-09-05', 200);
/* student 10 */
INSERT INTO matricula (id_estudiante, id_asignatura, num_matricula, fecha, precio)
VALUES (10, 8, 1, '2020-09-06', 100);
