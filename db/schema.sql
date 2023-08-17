-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 16-11-2020 a las 01:08:58
-- Versión del servidor: 10.4.14-MariaDB
-- Versión de PHP: 7.4.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `grupo69`
--
CREATE DATABASE IF NOT EXISTS `grupo69` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `grupo69`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `center`
--

DROP TABLE IF EXISTS `center`;
CREATE TABLE `center` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `address` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `phone` varchar(15) COLLATE utf8_unicode_ci NOT NULL,
  `opens` time NOT NULL,
  `closes` time NOT NULL,
  `town` int(255) NOT NULL,
  `web` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `protocol` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `longitude` varchar(127) COLLATE utf8_unicode_ci NOT NULL,
  `latitude` varchar(127) COLLATE utf8_unicode_ci NOT NULL,
  `center_state_id` int(11) NOT NULL,
  `center_type_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `center`
--

INSERT INTO `center` (`id`, `name`, `address`, `phone`, `opens`, `closes`, `town`, `web`, `email`, `protocol`, `longitude`, `latitude`, `center_state_id`, `center_type_id`) VALUES
(3, 'El Sol por las Mañanas', 'Calle 48 902-950, La Plata, B1900, Buenos Aires', '123-123-1234', '08:00:00', '19:00:00', 19, 'www.elsolporlasmañanas.com', 'elsolporlasmananas@ejemplo.com', '', '-57.95805215835572', '-34.919965313785035', 1, 1),
(4, 'Plasma para todes', 'Doctor Ángel R. Ferella 402-450, Ensenada, B1925, Buenos Aires', '234-234-2345', '08:00:00', '19:00:00', 7, '', '', '', '-57.9081416130066', '-34.85991171145938', 1, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `center_state`
--

DROP TABLE IF EXISTS `center_state`;
CREATE TABLE `center_state` (
  `id` int(11) NOT NULL,
  `name` varchar(45) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `center_state`
--

INSERT INTO `center_state` (`id`, `name`) VALUES
(1, 'Aprobado'),
(2, 'Pendiente'),
(3, 'Rechazado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `center_type`
--

DROP TABLE IF EXISTS `center_type`;
CREATE TABLE `center_type` (
  `id` int(11) NOT NULL,
  `name` varchar(45) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `center_type`
--

INSERT INTO `center_type` (`id`, `name`) VALUES
(1, 'Comida'),
(2, 'Sangre'),
(3, 'Ropa'),
(4, 'Plasma');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuration`
--

DROP TABLE IF EXISTS `configuration`;
CREATE TABLE `configuration` (
  `id` int(11) NOT NULL,
  `Title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `Description` text COLLATE utf8_unicode_ci NOT NULL,
  `Email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `ItemsPerPage` int(255) NOT NULL,
  `Enable` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `configuration`
--

INSERT INTO `configuration` (`id`, `Title`, `Description`, `Email`, `ItemsPerPage`, `Enable`) VALUES
(1, 'Donar', 'Vamos a Donar', 'donaciones@donar.com', 2, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permission`
--

DROP TABLE IF EXISTS `permission`;
CREATE TABLE `permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `permission`
--

INSERT INTO `permission` (`id`, `name`) VALUES
(0, 'turn_search'),
(1, 'user_index'),
(2, 'user_search'),
(3, 'user_delete'),
(4, 'user_state'),
(5, 'role_assign'),
(6, 'role_delete'),
(7, 'user_edit'),
(8, 'user_new'),
(9, 'configuration_update'),
(10, 'configuration_index'),
(11, 'role_select'),
(12, 'turn_index'),
(13, 'turn_create'),
(14, 'turn_delete'),
(15, 'turn_search'),
(16, 'center_index'),
(17, 'center_edit'),
(18, 'center_delete'),
(19, 'center_certify'),
(20, 'center_new'),
(21, 'center_create'),
(22, 'role_show');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `role`
--

DROP TABLE IF EXISTS `role`;
CREATE TABLE `role` (
  `id` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `role`
--

INSERT INTO `role` (`id`, `name`) VALUES
(1, 'admin'),
(2, 'operator');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles_have_permissions`
--

DROP TABLE IF EXISTS `roles_have_permissions`;
CREATE TABLE `roles_have_permissions` (
  `role_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `roles_have_permissions`
--

INSERT INTO `roles_have_permissions` (`role_id`, `permission_id`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(1, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 19),
(1, 20),
(1, 21),
(1, 22),
(2, 12),
(2, 13),
(2, 14),
(2, 15),
(2, 16),
(2, 17),
(2, 19),
(2, 20),
(2, 21);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `schedule`
--

DROP TABLE IF EXISTS `schedule`;
CREATE TABLE `schedule` (
  `id` int(11) NOT NULL,
  `start` time NOT NULL,
  `end` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `schedule`
--

INSERT INTO `schedule` (`id`, `start`, `end`) VALUES
(0, '09:00:00', '09:30:00'),
(1, '09:30:00', '10:00:00'),
(2, '10:00:00', '10:30:00'),
(3, '10:30:00', '11:00:00'),
(4, '11:00:00', '11:30:00'),
(5, '11:30:00', '12:00:00'),
(6, '12:00:00', '12:30:00'),
(7, '12:30:00', '13:00:00'),
(8, '13:00:00', '13:30:00'),
(9, '13:30:00', '14:00:00'),
(10, '14:00:00', '14:30:00'),
(11, '14:30:00', '15:00:00'),
(12, '15:00:00', '15:30:00'),
(13, '15:30:00', '16:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `turn`
--

DROP TABLE IF EXISTS `turn`;
CREATE TABLE `turn` (
  `id` int(11) NOT NULL,
  `email` varchar(45) COLLATE utf8_unicode_ci NOT NULL,
  `day` date NOT NULL,
  `center_id` int(11) NOT NULL,
  `schedule_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `turn`
--

INSERT INTO `turn` (`id`, `email`, `day`, `center_id`, `schedule_id`) VALUES
(21, 'juangomez@hotmail.com', '2020-11-19', 3, 2),
(22, 'cecilia_1978@gmail.com', '2020-11-23', 3, 5),
(23, 'flaviomendoza@outlook.com', '2020-11-20', 4, 10),
(24, 'gustavogustavez@hotmail.com', '2020-11-24', 4, 6),
(25, 'manuel@hotmail.com', '2020-11-16', 3, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

DROP TABLE IF EXISTS `user`;
CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `active` tinyint(1) NOT NULL,
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  `first_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `email`, `username`, `password`, `active`, `updated_at`, `created_at`, `first_name`, `last_name`) VALUES
(1, 'admin@ejemplo.com', 'admin', '$5$rounds=535000$FPTRYnDocqL2QLtJ$ucV/CMbVi996QEmMI.WDggwLX57XN3/iRfcCIYgMsJ1', 1, '2020-11-04 16:23:13', '2020-11-04 16:23:12', 'admin', 'istrador'),
(2, 'operator@ejemplo.com', 'operator', '$5$rounds=535000$W3hN6VJlXg8u3k5u$QzVWA9Eoe5NHwZXamJlA6uVb6lT/KJXGA4tyZYKA/Q.', 1, '2020-11-04 16:23:13', '2020-11-04 16:23:12', 'Ope', 'Rator');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users_have_roles`
--

DROP TABLE IF EXISTS `users_have_roles`;
CREATE TABLE `users_have_roles` (
  `role_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `users_have_roles`
--

INSERT INTO `users_have_roles` (`role_id`, `user_id`) VALUES
(1, 1),
(2, 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `center`
--
ALTER TABLE `center`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_center_center_state1` (`center_state_id`),
  ADD KEY `fk_center_center_type1` (`center_type_id`);

--
-- Indices de la tabla `center_state`
--
ALTER TABLE `center_state`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `center_type`
--
ALTER TABLE `center_type`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `permission`
--
ALTER TABLE `permission`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `roles_have_permissions`
--
ALTER TABLE `roles_have_permissions`
  ADD PRIMARY KEY (`role_id`,`permission_id`),
  ADD KEY `fk_role_has_permission_permission1` (`permission_id`);

--
-- Indices de la tabla `schedule`
--
ALTER TABLE `schedule`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `turn`
--
ALTER TABLE `turn`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_turn_center1` (`center_id`),
  ADD KEY `fk_turn_schedule1` (`schedule_id`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users_have_roles`
--
ALTER TABLE `users_have_roles`
  ADD PRIMARY KEY (`role_id`,`user_id`),
  ADD KEY `fk_user_has_role_user1` (`user_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `center`
--
ALTER TABLE `center`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `turn`
--
ALTER TABLE `turn`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `center`
--
ALTER TABLE `center`
  ADD CONSTRAINT `fk_center_center_state1` FOREIGN KEY (`center_state_id`) REFERENCES `center_state` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_center_center_type1` FOREIGN KEY (`center_type_id`) REFERENCES `center_type` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `roles_have_permissions`
--
ALTER TABLE `roles_have_permissions`
  ADD CONSTRAINT `fk_role_has_permission_permission1` FOREIGN KEY (`permission_id`) REFERENCES `permission` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_role_has_permission_role1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `turn`
--
ALTER TABLE `turn`
  ADD CONSTRAINT `fk_turn_center1` FOREIGN KEY (`center_id`) REFERENCES `center` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_turn_schedule1` FOREIGN KEY (`schedule_id`) REFERENCES `schedule` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `users_have_roles`
--
ALTER TABLE `users_have_roles`
  ADD CONSTRAINT `fk_user_has_role_role` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_user_has_role_user1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
