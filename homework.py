from dataclasses import asdict, dataclass
from typing import Dict, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    DURATION_IN_MINUTS_COEFF: float = 60

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'расход калорий расчитывается '
            'в дочернем классе ', self.__class__.__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    COEFF_MEAN_SPEED_1: float = 18
    COEFF_MEAN_SPEED_2: float = 20
    LEN_STEP: float = 0.65

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        return ((self.COEFF_MEAN_SPEED_1
                * self.get_mean_speed()
                - self.COEFF_MEAN_SPEED_2)
                * self.weight
                / self.M_IN_KM * self.duration * self.DURATION_IN_MINUTS_COEFF)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    LEN_STEP: float = 0.65
    COEFF_WEIGHT_CALORIES_1: float = 0.035
    COEFF_CALORIES_CONST_2: float = 2
    COEFF_WEIGHT_CALORIES_3: float = 0.029

    def __init__(
            self,
            action: float,
            duration: float,
            weight: float,
            height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для ходьбы."""

        return ((
            self.COEFF_WEIGHT_CALORIES_1
            * self.weight + (self.get_mean_speed()
                ** self.COEFF_CALORIES_CONST_2
                // self.height)
            * self.COEFF_WEIGHT_CALORIES_3
            * self.weight)
            * self.duration * self.DURATION_IN_MINUTS_COEFF)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    COEFF_CALORIES_CONST_SWM_1: float = 1.1
    COEFF_CALORIES_WEIGHT_SWM_2: float = 2

    def __init__(
            self,
            action: float,
            duration: float,
            weight: float,
            length_pool: float,
            count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения для плавания."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для плавания."""
        return ((
            self.get_mean_speed() + self.COEFF_CALORIES_CONST_SWM_1)
            * self.COEFF_CALORIES_WEIGHT_SWM_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    district_sport: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }

    if workout_type not in district_sport:
        raise KeyError(
            'ключа', workout_type, 'я не знаю,'
            'ведите другой код тренeровки')
    return district_sport[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
