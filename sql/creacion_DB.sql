create database estres_universitario;

use estres_universitario;

CREATE TABLE IF NOT EXISTS arquetipo (
    arquetipo_id   INT AUTO_INCREMENT PRIMARY KEY,
    nombre_arquetipo VARCHAR(50)  NOT NULL,
    descripcion    VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS usuario (
    usuario_id      INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario  VARCHAR(50)  NOT NULL,
    apellido_usuario VARCHAR(50) NOT NULL,
    correo_usuario  VARCHAR(100) NOT NULL UNIQUE,
    password_hash   VARCHAR(255) NOT NULL,
    rol             VARCHAR(30)  NOT NULL DEFAULT 'Estudiante',
    arquetipo_id    INT,
    FOREIGN KEY (arquetipo_id) REFERENCES arquetipo(arquetipo_id)
);

CREATE TABLE IF NOT EXISTS evento_academico (
    eventoAcademico_id INT AUTO_INCREMENT PRIMARY KEY,
    materia         VARCHAR(20)  NOT NULL,
    tipo            VARCHAR(20)  NOT NULL,
    fecha           DATE         NOT NULL,
    peso            DECIMAL(10,2) NOT NULL,
    estado          VARCHAR(30)  NOT NULL DEFAULT 'Pendiente',
    usuario_id      INT          NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(usuario_id)
);

CREATE TABLE IF NOT EXISTS registro_estres (
    registroEstres_id INT AUTO_INCREMENT PRIMARY KEY,
    nivel           INT          NOT NULL,
    causa           VARCHAR(40),
    fecha           DATE         NOT NULL,
    usuario_id      INT          NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(usuario_id)
);

CREATE TABLE IF NOT EXISTS tecnica_manejo_estres (
    tecnicaManejoEstres_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_tecnica  VARCHAR(50)  NOT NULL,
    descripcion     VARCHAR(255)  NOT NULL,
    arquetipo_id    INT          NOT NULL,
    FOREIGN KEY (arquetipo_id) REFERENCES arquetipo(arquetipo_id)
);

CREATE TABLE IF NOT EXISTS alerta (
    alerta_id       INT AUTO_INCREMENT PRIMARY KEY,
    estado          VARCHAR(30)  NOT NULL DEFAULT 'Pendiente',
    fecha           DATE         NOT NULL,
    mensaje         VARCHAR(100) NOT NULL,
    usuario_id      INT          NOT NULL,
    tecnicaManejoEstres_id INT   NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(usuario_id),
    FOREIGN KEY (tecnicaManejoEstres_id) REFERENCES tecnica_manejo_estres(tecnicaManejoEstres_id)
);



-- Arquetipos de manejo de estrés (los 5 que definiste)
INSERT INTO arquetipo (nombre_arquetipo, descripcion) VALUES
  ('Introspectivo', 'Enfoque Mental y Espiritual. Busca la calma a través del silencio, la reflexión profunda y la desconexión del ruido exterior. Prefiere actividades solitarias y espacios tranquilos.'),
  ('Kinestésico',   'Enfoque Físico. Procesa y libera el cortisol a través del movimiento del cuerpo. Acumula tensión en los músculos y siente frustración si pasa mucho tiempo sentado o inactivo.'),
  ('Creador',       'Enfoque Expresivo. Canaliza el estrés transformándolo en algo tangible a través del arte, la música o actividades manuales. Necesita un escape creativo.'),
  ('Analítico',     'Enfoque de Control. Reduce el estrés organizando, planificando y resolviendo los problemas de raíz. Su estrés proviene de la incertidumbre o el caos.'),
  ('Social',        'Enfoque de Conexión. Alivia la carga emocional compartiendo sentimientos y buscando apoyo de su comunidad. La soledad prolongada aumenta su ansiedad.');

-- Técnicas del Introspectivo (arquetipo_id = 1)
INSERT INTO tecnica_manejo_estres (nombre_tecnica, descripcion, arquetipo_id) VALUES
  ('Meditación mindfulness', 'Práctica de atención plena para calmar la mente y reducir el ruido mental.', 1),
  ('Journaling',             'Escritura terapéutica: poner en palabras lo que se siente para procesarlo.', 1),
  ('Respiración Pranayama',  'Ejercicios de respiración profunda para regular el sistema nervioso.', 1),
  ('Retiro en naturaleza',   'Desconexión en espacios naturales y silenciosos, lejos del ruido exterior.', 1);

-- Técnicas del Kinestésico (arquetipo_id = 2)
INSERT INTO tecnica_manejo_estres (nombre_tecnica, descripcion, arquetipo_id) VALUES
  ('Ejercicio alta intensidad', 'Correr, boxeo o HIIT para liberar cortisol a través del movimiento.', 2),
  ('Yoga dinámico / Qi Gong',   'Práctica consciente en movimiento que combina cuerpo y respiración.', 2),
  ('Caminata al aire libre',    'Caminata a paso ligero para descargar tensión acumulada en el cuerpo.', 2),
  ('Masaje de descarga',        'Masaje corporal para liberar tensión muscular acumulada por el estrés.', 2);

-- Técnicas del Creador (arquetipo_id = 3)
INSERT INTO tecnica_manejo_estres (nombre_tecnica, descripcion, arquetipo_id) VALUES
  ('Pintar o colorear',       'Pintar, dibujar o colorear mandalas como escape creativo.', 3),
  ('Tocar un instrumento',    'Tocar un instrumento musical para canalizar emociones.', 3),
  ('Cocinar o jardinería',    'Actividades manuales relajantes: cocinar o cuidar plantas.', 3),
  ('Manualidades',            'Cerámica, tejido u otras manualidades como vía de expresión.', 3);

-- Técnicas del Analítico (arquetipo_id = 4)
INSERT INTO tecnica_manejo_estres (nombre_tecnica, descripcion, arquetipo_id) VALUES
  ('Método Pomodoro',          'Técnica de gestión del tiempo en bloques para dar estructura al día.', 4),
  ('Lista de prioridades',     'Hacer listas de tareas prioritarias (To-Do lists) para reducir incertidumbre.', 4),
  ('Organizar espacio físico', 'Limpieza y organización del espacio de estudio o trabajo.', 4),
  ('Lectura de autoayuda',     'Lectura de libros de desarrollo personal y gestión del estrés.', 4);

-- Técnicas del Social (arquetipo_id = 5)
INSERT INTO tecnica_manejo_estres (nombre_tecnica, descripcion, arquetipo_id) VALUES
  ('Hablar con alguien de confianza', 'Conversar con amigos cercanos o familiares sobre las preocupaciones.', 5),
  ('Actividad grupal',                'Participar en actividades grupales o voluntariados.', 5),
  ('Terapia psicológica',             'Acompañamiento profesional: coaching o psicoterapia.', 5),
  ('Tiempo con seres queridos',       'Pasar tiempo o abrazar a seres queridos y mascotas.', 5);


INSERT INTO usuario (nombre_usuario, apellido_usuario, correo_usuario, password_hash, rol, arquetipo_id)
VALUES ('Admin', 'Sistema', 'admin@udla.edu.ec', 'scrypt:32768:8:1$hAacb44bqPX2bfDI$c25bd264a7d641a156e493281d816c9203f79cd5f93a531f3a3c8b9e809f7fc725f06e2f5bcd23f6e02536f710e8250f5266d05623fa53fd16be2297052e7a54', 'Administrador', NULL);

