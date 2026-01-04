-- Obtener todos los registros de la tabla de matriculas
SELECT *
FROM matricula

-- Insertar un nuevo estudiante con id_estudiante = 999, con nombre 'Marcos' y dirección 'La Paz'
INSERT INTO estudiante (id_estudiante, nombre, direccion)
VALUES (999, 'Marcos', 'La Paz')
-- Obtener el estudiante con id_estudiante = 999
SELECT FROM estudiante
WHERE id_estudiante = 999

-- Obtener todas las asignaturas con más de 6 créditos
SELECT id_asignatura
FROM asignatura
WHERE creditos> 6

-- Obtener todas las matrículas realizadas por el estudiante con id_estudiante = 1
SELECT *
FROM matricula
WHERE id_estudiante = 1

-- Para cada matrícula realizada obtener: id_estudiante, nombre_estudiante, id_asignatura, num_matricula, fecha y precio
SELECT matricula.id_estudiante, matricula.id_asignatura, matricula.num_matricula, matricula.fecha, matricula.precio, estudiante.nombre
FROM matricula
JOIN estudiante ON matricula.id_estudiante=estudiante.id_estudiante

-- Para cada matrícula realizada obtener: id_estudiante, nombre_estudiante, id_asignatura, num_matricula, fecha, precio, creditos_asignatura y titulo_asignatura
SELECT matricula.id_estudiante, matricula.id_asignatura, matricula.num_matricula, matricula.fecha, matricula.precio, estudiante.nombre, asignatura.creditos, asignatura.titulo
FROM matricula
LEFT JOIN estudiante ON matricula.id_estudiante=estudiante.id_estudiante
LEFT JOIN asignatura ON matricula.id_asignatura=asignatura.id_asignatura

-- Obtener el id y el nombre del estudiante, junto a una lista de fechas de matrícula para cada matrícula realizada (sin repetidos), agrupados por estudiante
-- Si un estudiante tiene estas 4 fechas de matricula (2020-09-01, 2020-09-02, 2020-09-01, 2020-09-03), la lista de fechas de matrícula deberá ser (2020-09-01, 2020-09-02, 2020-09-03)
SELECT matricula.id_estudiante, matricula.fecha, estudiante.nombre
FROM matricula
Left JOIN estudiante ON matricula.id_estudiante=estudiante.id_estudiante
Left JOIN asignatura ON 
GROUP BY nombre

-- Obtener todos los profesores que trabajan en el departamento de 'Ingenieria', sin especifica directamente el id del departamento en la query SQL
SELECT profesor.nombre
FROM profesor
WHERE profesor.especialidad IN ('Programacion', 'Robotica', 'Sistemas Distribuidos')

-- Añadir una nueva columna opcional a la tabla estudiante: DNI
ALTER TABLE estudiante
ADD COLUMN dni VARCHAR(9)
-- Modificar los estudiantes con ids 1, 2 y 3 para añadirles un DNI (12345678A, 12345678B, 12345678C respectivamente)
UPDATE estudiante
SET dni = CASE id_estudiante
             WHEN 1 THEN '12345678A'
             WHEN 2 THEN '12345678B'
             WHEN 3 THEN '12345678C'
          END
WHERE id_estudiante IN (1, 2, 3);

-- Revisar los datos de todos los estudiantes
SELECT *
FROM estudiante

-- Obtener las matrículas realizadas entre el 3 de septiembre de 2020 y el 5 de septiembre de 2020 (ambos inclusive)
SELECT *
FROM matricula
WHERE fecha BETWEEN '2020-09-03' AND '2020-09-05'

-- Obtener el número de matriculas realizadas entre el 3 de septiembre de 2020 y el 5 de septiembre de 2020 (ambos inclusive)
SELECT COUNT(matricula.num_matricula)
FROM matricula
WHERE fecha BETWEEN '2020-09-03' AND '2020-09-05'

-- Obtener las asignaturas con más de 6 créditos ordenadas por título alfabéticamente, junto a la cantidad de matrículas
SELECT 
    asignatura.titulo, 
    COUNT(matricula.id_asignatura) AS cantidad_matriculas
FROM 
    asignatura
LEFT JOIN 
    matricula ON asignatura.id_asignatura = matricula.id_asignatura
WHERE 
    asignatura.creditos > 6
GROUP BY 
    asignatura.titulo
ORDER BY 
    asignatura.titulo ASC;


-- Obtener el número de matrículas realizadas por cada estudiante (de aquellos que han realizado al menos una matrícula),
-- ordenados por número de matrículas de forma descendente
SELECT 
    estudiante.nombre, 
    COUNT(matricula.num_matricula) AS num_matriculas
FROM 
    estudiante
JOIN 
    matricula ON estudiante.id_estudiante = matricula.id_estudiante
GROUP BY 
    estudiante.nombre
ORDER BY 
    num_matriculas DESC;


-- Obtener el número de matrículas realizadas por cada estudiante (de todos los estudiantes, aunque no hayan realizado ninguna matrícula),
-- ordenados por número de matrículas de forma descendente
SELECT estudiante.nombre, COUNT(matricula.num_matricula)
FROM estudiante
LEFT JOIN matricula ON estudiante.id_estudiante=matricula.id_estudiante
GROUP BY estudiante.nombre
HAVING count(MATRICULA.num_matricula) >= 0
ORDER BY count(MATRICULA.num_matricula) DESC;

-- Obtener la cantidad de dinero gastada por cada estudiante (de todos los estudiantes, aunque no hayan realizado ninguna matrícula)
-- ordenados por cantidad de dinero gastada de forma descendente
SELECT estudiante.nombre, COUNT(matricula.num_matricula)
FROM estudiante
LEFT JOIN matricula ON estudiante.id_estudiante=matricula.id_estudiante
GROUP BY estudiante.nombre
HAVING count(MATRICULA.num_matricula) >= 0
ORDER BY count(MATRICULA.num_matricula) DESC;

-- Obtener la cantidad de dinero gastada por cada estudiante
-- ordenados por cantidad de dinero gastada de forma descendente, de aquellos que han gastado más de 200€
SELECT estudiante.nombre, count(matricula.num_matricula), sum(matricula.precio)
FROM estudiante
LEFT JOIN matricula ON estudiante.id_estudiante=matricula.id_estudiante
GROUP BY estudiante.nombre
HAVING sum(matricula.precio) >= 200
ORDER BY sum(matricula.precio) DESC;

-- Obtener la asignatura más cara que ha matriculado cada estudiante (id_estudiante, nombre_estudiante, asignatura_mas_cara (su titulo), precio)
-- Nota: Si varias asignaturas tienen el mismo precio, se mostrará la primera que se encuentre en la tabla
SELECT estudiante.nombre, estudiante.nombre, matricula.precio, asignatura.titulo
FROM estudiante
LEFT JOIN matricula ON estudiante.id_estudiante=matricula.id_estudiante
Left JOIN asignatura ON matricula.id_asignatura=asignatura.id_asignatura
GROUP BY estudiante.nombre
ORDER BY matricula.precio DESC;

-- Obtener la información de la relación entre estudiantes y profesores (para todos los estudiantes y profesores,
-- aunque los estudiantes no hayan realizado ninguna matrícula y los profesores no hayan impartido ninguna asignatura)
-- (id_estudiante, nombre_estudiante, id_asignatura, nombre_asignatura, id_profesor, nombre_profesor, nombre_departamento)
SELECT 
    estudiante.id_estudiante, 
    estudiante.nombre AS nombre_estudiante, 
    asignatura.id_asignatura, 
    asignatura.titulo AS nombre_asignatura, 
    profesor.id_profesor, 
    profesor.nombre AS nombre_profesor, 
    departamento.nombre AS nombre_departamento
FROM estudiante
LEFT JOIN matricula ON estudiante.id_estudiante = matricula.id_estudiante
LEFT JOIN asignatura ON matricula.id_asignatura = asignatura.id_asignatura
LEFT JOIN profesor ON asignatura.id_profesor = profesor.id_profesor
LEFT JOIN departamento ON profesor.id_departamento = departamento.id_departamento
ORDER BY estudiante.id_estudiante, asignatura.id_asignatura, profesor.id_profesor;

-- Obtener, por cada departamento, el número de profesores que trabajan en él, el número de asignaturas que imparten, el número de matrículas realizadas
-- y el número de estudiantes matriculados,ordenados por id del departamento de forma ascendente
-- (nombre_departamento, num_profesores, num_asignaturas, num_matriculas, num_estudiantes_matriculados)
SELECT 
    departamento.nombre AS nombre_departamento,
    COUNT(DISTINCT profesor.id_profesor) AS num_profesores,
    COUNT(DISTINCT asignatura.id_asignatura) AS num_asignaturas,
    COUNT(DISTINCT matricula.num_matricula) AS num_matriculas,
    COUNT(DISTINCT matricula.id_estudiante) AS num_estudiantes_matriculados
FROM departamento
LEFT JOIN profesor ON departamento.id_departamento = profesor.id_departamento
LEFT JOIN asignatura ON profesor.id_profesor = asignatura.id_profesor
LEFT JOIN matricula ON asignatura.id_asignatura = matricula.id_asignatura
GROUP BY 
    departamento.id_departamento, departamento.nombre
ORDER BY 
    departamento.id_departamento ASC;
