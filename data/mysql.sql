CREATE DATABASE zendesk;

DROP TABLE IF EXISTS zendesk.RutinasDisponibles;
CREATE TABLE zendesk.RutinasDisponibles (
  id INT NOT NULL AUTO_INCREMENT,
  NombreRutina VARCHAR(45) NULL,
  DescripcionRutina VARCHAR(250) NULL,
  idVistaZendesk VARCHAR(45) NULL,
  NombreVistaZendesk VARCHAR(45) NULL,
  idAlgoritmo INT NULL,
  esActivado INT NULL,
  ultimoCambioEstado VARCHAR(45) NULL,
  Etiquetas VARCHAR(250) NULL,
  PRIMARY KEY (id));

DROP TABLE IF EXISTS zendesk.CargaAgentes;
CREATE TABLE zendesk.CargaAgentes (
  id INT NOT NULL AUTO_INCREMENT,
  idAgenteZendesk BIGINT NULL,
  idRutina INT NULL,
  esActivado INT NULL,
  ultimoCambioEstado VARCHAR(45) NULL,
  marcadorTurno INT NULL DEFAULT 0,
  cargaTrabajo INT NULL DEFAULT 0,
  PRIMARY KEY (id),
  FOREIGN KEY (idRutina) REFERENCES RutinasDisponibles(id)
);

DROP TABLE IF EXISTS zendesk.AlgoritmosDisponibles;
CREATE TABLE zendesk.AlgoritmosDisponibles (
	id INT NOT NULL AUTO_INCREMENT,
	nombreAlgoritmo VARCHAR(45) NULL,
	descripcionAlgoritmo VARCHAR(250) NULL,
	nombreArchivo VARCHAR(45) NULL,
PRIMARY KEY (id));

INSERT INTO zendesk.AlgoritmosDisponibles (nombreAlgoritmo, descripcionAlgoritmo, nombreArchivo) VALUES ('ReparticiÃ³n en ronda', 'Reparte haciendo una ronda entre los usuarios asociados, no considera dificultad de la pregunta ni criterios de equidad', 'roundRobin_classic.py');

DROP VIEW IF EXISTS zendesk.RutinasDisponiblesTotAgentes;
CREATE VIEW zendesk.RutinasDisponiblesTotAgentes AS
SELECT a.id, a.NombreRutina, a.DescripcionRutina, a.idVistaZendesk,a.NombreVistaZendesk, a.idAlgoritmo, a.esActivado, a.ultimoCambioEstado, b.totagentes FROM zendesk.RutinasDisponibles AS a
LEFT JOIN (SELECT c.idRutina, count(c.idAgenteZendesk) AS totagentes FROM zendesk.CargaAgentes as c GROUP BY c.idRutina) AS b ON a.id=b.idRutina;
