-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Хост: 127.0.0.1
-- Время создания: Июн 03 2026 г., 21:08
-- Версия сервера: 10.4.32-MariaDB
-- Версия PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `chitaigorod`
--
CREATE DATABASE IF NOT EXISTS `chitaigorod` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `chitaigorod`;

-- --------------------------------------------------------

--
-- Структура таблицы `categories`
--

DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `category_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `categories`
--

INSERT INTO `categories` (`category_id`, `name`) VALUES
(1, 'Художественная литература'),
(2, 'Учебник для вузов'),
(3, 'Хрестоматия'),
(4, 'Учебное пособие');

-- --------------------------------------------------------

--
-- Структура таблицы `manufacturers`
--

DROP TABLE IF EXISTS `manufacturers`;
CREATE TABLE `manufacturers` (
  `manufacturer_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `manufacturers`
--

INSERT INTO `manufacturers` (`manufacturer_id`, `name`) VALUES
(1, 'Яуза'),
(2, 'Т8 Издательские технологии'),
(3, 'Прогресс книга'),
(4, 'Время'),
(5, 'Лениздат'),
(6, 'Неолит'),
(7, 'Амрита-Русь'),
(8, 'Златоуст'),
(9, 'Аспект Пресс'),
(10, 'ВКН');

-- --------------------------------------------------------

--
-- Структура таблицы `orders`
--

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `order_date` date DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `pvz_id` int(11) NOT NULL,
  `client_fio_id` int(11) DEFAULT NULL,
  `pickup_code` int(11) DEFAULT NULL,
  `status_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `orders`
--

INSERT INTO `orders` (`order_id`, `order_date`, `delivery_date`, `pvz_id`, `client_fio_id`, `pickup_code`, `status_id`) VALUES
(1, '2024-02-27', '2024-04-20', 1, 10, 901, 1),
(2, '2023-09-28', '2024-04-21', 11, 7, 902, 1),
(3, '2024-03-21', '2024-04-22', 2, 8, 903, 1),
(4, '2024-02-20', '2024-04-23', 11, 9, 904, 1),
(5, '2024-03-17', '2024-04-24', 2, 10, 905, 1),
(6, '2024-03-01', '2024-04-25', 15, 7, 906, 1),
(7, '2024-02-28', '2024-04-26', 3, 8, 907, 1),
(8, '2024-03-31', '2024-04-27', 19, 9, 908, 2),
(9, '2024-04-02', '2024-04-28', 5, 10, 909, 2),
(10, '2024-04-03', '2024-04-29', 19, 10, 910, 2);

-- --------------------------------------------------------

--
-- Структура таблицы `order_items`
--

DROP TABLE IF EXISTS `order_items`;
CREATE TABLE `order_items` (
  `order_item_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `article` varchar(6) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `order_items`
--

INSERT INTO `order_items` (`order_item_id`, `order_id`, `article`, `quantity`) VALUES
(1, 1, 'А112Т4', 2),
(2, 1, 'G843H5', 2),
(3, 2, 'G843H5', 1),
(4, 2, 'А112Т4', 1),
(5, 3, 'D325D4', 10),
(6, 3, 'S432T5', 10),
(7, 4, 'F325D4', 5),
(8, 4, 'D325D4', 4),
(9, 5, 'G432G6', 20),
(10, 5, 'H542F5', 20),
(11, 6, 'А112Т4', 2),
(12, 6, 'G843H5', 2),
(13, 7, 'C346F5', 3),
(14, 7, 'F256G6', 3),
(15, 8, 'F325D4', 1),
(16, 8, 'G432G6', 1),
(17, 9, 'J532V5', 5),
(18, 9, 'F256G6', 1),
(19, 10, 'F256G6', 5),
(20, 10, 'J532V5', 5);

-- --------------------------------------------------------

--
-- Структура таблицы `order_status`
--

DROP TABLE IF EXISTS `order_status`;
CREATE TABLE `order_status` (
  `status_id` int(11) NOT NULL,
  `name` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `order_status`
--

INSERT INTO `order_status` (`status_id`, `name`) VALUES
(1, 'Завершен'),
(2, 'Новый');

-- --------------------------------------------------------

--
-- Структура таблицы `pvz`
--

DROP TABLE IF EXISTS `pvz`;
CREATE TABLE `pvz` (
  `pvz_id` int(11) NOT NULL,
  `address` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `pvz`
--

INSERT INTO `pvz` (`pvz_id`, `address`) VALUES
(1, '420151, г. Лесной, ул. Вишневая, 32'),
(2, '125061, г. Лесной, ул. Подгорная, 8'),
(3, '630370, г. Лесной, ул. Шоссейная, 24'),
(4, '400562, г. Лесной, ул. Зеленая, 32'),
(5, '614510, г. Лесной, ул. Маяковского, 47'),
(6, '410542, г. Лесной, ул. Светлая, 46'),
(7, '620839, г. Лесной, ул. Цветочная, 8'),
(8, '443890, г. Лесной, ул. Коммунистическая, 1'),
(9, '603379, г. Лесной, ул. Спортивная, 46'),
(10, '603721, г. Лесной, ул. Гоголя, 41'),
(11, '410172, г. Лесной, ул. Северная, 13'),
(12, '614611, г. Лесной, ул. Молодежная, 50'),
(13, '454311, г.Лесной, ул. Новая, 19'),
(14, '660007, г.Лесной, ул. Октябрьская, 19'),
(15, '603036, г. Лесной, ул. Садовая, 4'),
(16, '394060, г.Лесной, ул. Фрунзе, 43'),
(17, '410661, г. Лесной, ул. Школьная, 50'),
(18, '625590, г. Лесной, ул. Коммунистическая, 20'),
(19, '625683, г. Лесной, ул. 8 Марта'),
(20, '450983, г.Лесной, ул. Комсомольская, 26'),
(21, '394782, г. Лесной, ул. Чехова, 3'),
(22, '603002, г. Лесной, ул. Дзержинского, 28'),
(23, '450558, г. Лесной, ул. Набережная, 30'),
(24, '344288, г. Лесной, ул. Чехова, 1'),
(25, '614164, г.Лесной,  ул. Степная, 30'),
(26, '394242, г. Лесной, ул. Коммунистическая, 43'),
(27, '660540, г. Лесной, ул. Солнечная, 25'),
(28, '125837, г. Лесной, ул. Шоссейная, 40'),
(29, '125703, г. Лесной, ул. Партизанская, 49'),
(30, '625283, г. Лесной, ул. Победы, 46'),
(31, '614753, г. Лесной, ул. Полевая, 35'),
(32, '426030, г. Лесной, ул. Маяковского, 44'),
(33, '450375, г. Лесной ул. Клубная, 44'),
(34, '625560, г. Лесной, ул. Некрасова, 12'),
(35, '630201, г. Лесной, ул. Комсомольская, 17'),
(36, '190949, г. Лесной, ул. Мичурина, 26');

-- --------------------------------------------------------

--
-- Структура таблицы `suppliers`
--

DROP TABLE IF EXISTS `suppliers`;
CREATE TABLE `suppliers` (
  `supplier_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `suppliers`
--

INSERT INTO `suppliers` (`supplier_id`, `name`) VALUES
(1, 'Виктор Астафьев'),
(2, 'Гилберт Кит Честертон'),
(3, 'Кирилл Каланджи'),
(4, 'Людмила Улицкая'),
(5, 'Аркадий Гайдар'),
(6, 'Юрий Родичев'),
(7, 'Дэниел Джей Барретт'),
(8, 'Шон Кэрролл'),
(9, 'Яков Гордин'),
(10, 'Иосиф Бродский'),
(11, 'Янь Чуннянь'),
(12, 'Дмитрий Мережковский'),
(13, 'Дмитрий Щербаков'),
(14, 'Роджер Осборн, Дэн Стерджис'),
(15, 'Любовь Беликова, Инна Ерофеева, Татьяна Шутова'),
(16, 'Сергей Моргачев'),
(17, 'Екатерина Габарта, Ирина Игнатьева'),
(18, 'Татьяна Лопаткина, Софья Маннапова');

-- --------------------------------------------------------

--
-- Структура таблицы `tovar`
--

DROP TABLE IF EXISTS `tovar`;
CREATE TABLE `tovar` (
  `article` varchar(6) NOT NULL,
  `name` varchar(200) NOT NULL,
  `unit_id` int(11) NOT NULL DEFAULT 1,
  `price` int(11) NOT NULL,
  `supplier_id` int(11) NOT NULL,
  `manufacturer_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `discount` int(11) DEFAULT 0,
  `stock_quantity` int(11) DEFAULT 0,
  `description` varchar(500) DEFAULT NULL,
  `image_path` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `tovar`
--

INSERT INTO `tovar` (`article`, `name`, `unit_id`, `price`, `supplier_id`, `manufacturer_id`, `category_id`, `discount`, `stock_quantity`, `description`, `image_path`) VALUES
('B653G6', 'Русский язык: Первые шаги. Часть 3. Учебное пособие', 1, 2699, 15, 8, 4, 8, 9, 'Пособие является завершающей частью учебного комплекса.', '17.jpg'),
('C346F5', 'Квантовые миры и возникновение пространства-времени', 1, 1349, 8, 3, 2, 5, 4, 'Шон Кэрролл — физик-теоретик и один из самых известных в мире популяризаторов науки.', '8.jpg'),
('D325D4', 'Девайс', 1, 1599, 3, 2, 1, 5, 12, 'Молодой фрилансер Захар Скаро устраивается на очередную подработку.', '3.jpg'),
('F256G6', 'Вселенная. Происхождение жизни, смысл нашего существования и огромный космос', 1, 1799, 8, 3, 2, 6, 2, 'Знаменитый физик Шон Кэрролл в свойственной ему увлекательной манере объясняет принципы.', ''),
('F325D4', 'Чук и Гек', 1, 209, 5, 2, 1, 18, 3, 'В книгу вошли повести и рассказы Аркадия Петровича Гайдара: \"Чук и Гек\", \"Горячий камень\" и \"Сказка о военной тайне...\"', '5.jpg'),
('G432G6', 'Информационная безопасность. Национальные стандарты Российской Федерации. 3-е издание. Учебное пособие', 1, 3899, 6, 3, 2, 22, 3, 'В учебном пособии рассмотрено более 300 действующих открытых документов национальной системы стандартизации.', '6.jpg'),
('G543F5', 'Религиозные верования с древнейших времен до наших дней', 1, 879, 13, 7, 3, 4, 6, 'Настоящее издание представляет собой сборник переводов лекций по истории религий.', '16.jpg'),
('G632H6', 'Формирование литературной репутации Н.Г.Чернышевского в ХIX-XXI веках', 1, 1349, 13, 6, 3, 2, 8, 'Монография Д. А. Щербакова - новаторская.', '14.jpg'),
('G643F4', 'Иосиф Бродский. Избранные эссе (комплект из 6-ти книг)', 1, 4925, 10, 5, 3, 2, 24, 'Шесть сборников избранных эссе Иосифа Бродского (1940-1996).', '11.jpg'),
('G843H5', 'Тайны и загадки отца Брауна', 1, 193, 2, 1, 1, 30, 9, 'Гилберт Кит Честертон — признанный классик английской литературы, один из самых ярких писателей первой половины XX века.', '2.jpg'),
('H436H7', 'Английский язык в спорте: Учебное пособие', 1, 1999, 17, 9, 4, 2, 0, 'Учебное пособие подготовлено для слушателей, изучающих английский язык как язык специальности.', '19.jpg'),
('H475R5', 'Лексика и грамматика современного китайского языка', 1, 608, 18, 10, 4, 25, 12, 'Пособие выступает дополнением ко второму тому учебника «Новый практический курс китайского языка».', '20.jpg'),
('H542F5', 'Linux. Командная строка. Лучшие практики', 1, 1799, 7, 3, 2, 4, 5, 'Перейдите на новый уровень работы в Linux!', '7.jpg'),
('J326V5', 'Тысячелетие императорской керамики', 1, 2599, 11, 5, 3, 5, 4, 'Фарфор стал величайшим символом китайской культуры.', '12.jpg'),
('J532V5', 'Пушкин. Бродский. Империя и судьба. В 2-х томах (комплект из 2-х книг)', 1, 529, 9, 4, 3, 8, 6, 'Первая книга двухтомника «Пушкин. Бродский. Империя и судьба» пронизана пушкинской темой.', '10.jpg'),
('J632F6', 'Вечные спутники: Портреты из всемирной литературы', 1, 1599, 12, 5, 3, 0, 6, 'Книга \"Вечные спутники\" - это цикл критических очерков о культуре и великих литераторах.', '13.jpg'),
('J735J7', 'Синтетический образ индивидуального психического мира', 1, 1099, 16, 8, 3, 9, 4, 'Психика подобна определенным объектам.', '18.jpg'),
('M642E5', 'Теория искусства. Краткий путеводитель', 1, 879, 14, 6, 3, 3, 2, '', '15.jpg'),
('S432T5', 'Необыкновенное обыкновенное чудо. Школьные истории', 1, 549, 4, 2, 1, 15, 15, '', '4.jpg'),
('А112Т4', 'Прокляты и убиты', 1, 585, 1, 1, 1, 25, 6, 'Роман-эпопею \"Прокляты и убиты\" Виктора Астафьева по праву считают одним из самых сильных и пронзительных произведений отечественной военной прозы.', '1.jpg');

-- --------------------------------------------------------

--
-- Структура таблицы `unit`
--

DROP TABLE IF EXISTS `unit`;
CREATE TABLE `unit` (
  `unit_id` int(11) NOT NULL,
  `name` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `unit`
--

INSERT INTO `unit` (`unit_id`, `name`) VALUES
(1, 'шт.');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `role` int(11) NOT NULL,
  `fio` int(11) NOT NULL,
  `login` varchar(50) NOT NULL,
  `password` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`user_id`, `role`, `fio`, `login`, `password`) VALUES
(1, 1, 1, '94d5ous@gmail.com', 'uzWC67'),
(2, 1, 2, 'uth4iz@mail.com', '2L6KZG'),
(3, 1, 3, '5d4zbu@tutanota.com', 'rwVDh9'),
(4, 2, 4, 'ptec8ym@yahoo.com', 'LdNyos'),
(5, 2, 5, '1qz4kw@mail.com', 'gynQMT'),
(6, 2, 6, '4np6se@mail.com', 'AtnDjr'),
(7, 3, 7, 'yzls62@outlook.com', 'JlFRCZ'),
(8, 3, 8, '1diph5e@tutanota.com', '8ntwUp'),
(9, 3, 9, 'tjde7c@yahoo.com', 'YOyhfR'),
(10, 3, 10, 'wpmrc3do@tutanota.com', 'RSbvHv'),
(11, 1, 1, '1@yahoo.com', '1'),
(12, 2, 4, '2@yahoo.com', '2'),
(13, 3, 10, '3@yahoo.com', '3');

-- --------------------------------------------------------

--
-- Структура таблицы `user_fio`
--

DROP TABLE IF EXISTS `user_fio`;
CREATE TABLE `user_fio` (
  `fio_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `user_fio`
--

INSERT INTO `user_fio` (`fio_id`, `name`) VALUES
(1, 'Никифорова Анна Семеновна'),
(2, 'Стелина Евгения Петровна'),
(3, 'Михайлюк Анна Вячеславовна'),
(4, 'Ситдикова Елена Анатольевна'),
(5, 'Ворсин Петр Евгеньевич'),
(6, 'Старикова Елена Павловна'),
(7, 'Никифорова Весения Николаевна'),
(8, 'Сазонов Руслан Германович'),
(9, 'Одинцов Серафим Артёмович'),
(10, 'Степанов Михаил Артёмович');

-- --------------------------------------------------------

--
-- Структура таблицы `user_roles`
--

DROP TABLE IF EXISTS `user_roles`;
CREATE TABLE `user_roles` (
  `role_id` int(11) NOT NULL,
  `name` varchar(23) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Дамп данных таблицы `user_roles`
--

INSERT INTO `user_roles` (`role_id`, `name`) VALUES
(1, 'Администратор'),
(2, 'Менеджер'),
(3, 'Авторизированный клиент');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`category_id`);

--
-- Индексы таблицы `manufacturers`
--
ALTER TABLE `manufacturers`
  ADD PRIMARY KEY (`manufacturer_id`);

--
-- Индексы таблицы `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `pvz_id` (`pvz_id`),
  ADD KEY `client_fio_id` (`client_fio_id`),
  ADD KEY `status_id` (`status_id`);

--
-- Индексы таблицы `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`order_item_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `article` (`article`);

--
-- Индексы таблицы `order_status`
--
ALTER TABLE `order_status`
  ADD PRIMARY KEY (`status_id`);

--
-- Индексы таблицы `pvz`
--
ALTER TABLE `pvz`
  ADD PRIMARY KEY (`pvz_id`);

--
-- Индексы таблицы `suppliers`
--
ALTER TABLE `suppliers`
  ADD PRIMARY KEY (`supplier_id`);

--
-- Индексы таблицы `tovar`
--
ALTER TABLE `tovar`
  ADD PRIMARY KEY (`article`),
  ADD KEY `unit_id` (`unit_id`),
  ADD KEY `supplier_id` (`supplier_id`),
  ADD KEY `manufacturer_id` (`manufacturer_id`),
  ADD KEY `category_id` (`category_id`);

--
-- Индексы таблицы `unit`
--
ALTER TABLE `unit`
  ADD PRIMARY KEY (`unit_id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `login` (`login`),
  ADD KEY `role` (`role`),
  ADD KEY `fio` (`fio`);

--
-- Индексы таблицы `user_fio`
--
ALTER TABLE `user_fio`
  ADD PRIMARY KEY (`fio_id`);

--
-- Индексы таблицы `user_roles`
--
ALTER TABLE `user_roles`
  ADD PRIMARY KEY (`role_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `categories`
--
ALTER TABLE `categories`
  MODIFY `category_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT для таблицы `manufacturers`
--
ALTER TABLE `manufacturers`
  MODIFY `manufacturer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `order_items`
--
ALTER TABLE `order_items`
  MODIFY `order_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT для таблицы `order_status`
--
ALTER TABLE `order_status`
  MODIFY `status_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT для таблицы `pvz`
--
ALTER TABLE `pvz`
  MODIFY `pvz_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT для таблицы `suppliers`
--
ALTER TABLE `suppliers`
  MODIFY `supplier_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT для таблицы `unit`
--
ALTER TABLE `unit`
  MODIFY `unit_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT для таблицы `user_fio`
--
ALTER TABLE `user_fio`
  MODIFY `fio_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT для таблицы `user_roles`
--
ALTER TABLE `user_roles`
  MODIFY `role_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`pvz_id`) REFERENCES `pvz` (`pvz_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`client_fio_id`) REFERENCES `user_fio` (`fio_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`status_id`) REFERENCES `order_status` (`status_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`article`) REFERENCES `tovar` (`article`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `tovar`
--
ALTER TABLE `tovar`
  ADD CONSTRAINT `tovar_ibfk_1` FOREIGN KEY (`unit_id`) REFERENCES `unit` (`unit_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tovar_ibfk_2` FOREIGN KEY (`supplier_id`) REFERENCES `suppliers` (`supplier_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tovar_ibfk_3` FOREIGN KEY (`manufacturer_id`) REFERENCES `manufacturers` (`manufacturer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `tovar_ibfk_4` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ограничения внешнего ключа таблицы `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role`) REFERENCES `user_roles` (`role_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `users_ibfk_2` FOREIGN KEY (`fio`) REFERENCES `user_fio` (`fio_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
