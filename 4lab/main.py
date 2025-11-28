from abc import ABC, abstractmethod
from typing import List, Dict, Any


class User(ABC):   
    @abstractmethod
    def get_id(self) -> int:
        pass
    
    @abstractmethod
    def get_full_name(self) -> str:
        pass
    
    @abstractmethod
    def get_email(self) -> str:
        pass
    
    @abstractmethod
    def get_info(self) -> Dict[str, str]:
        pass


class CSVUser(User):
    def __init__(self, csv_line: str):
        parts = csv_line.strip().replace('<csv ', '').replace('>', '').split(';')
        self.uid = int(parts[0])
        self.full_name = parts[1].strip()
        self.email = parts[2].strip()
    
    def get_id(self) -> int:
        return self.uid
    
    def get_full_name(self) -> str:
        return self.full_name
    
    def get_email(self) -> str:
        return self.email
    
    def get_info(self) -> Dict[str, str]:
        return {
            'id': str(self.uid),
            'full_name': self.full_name,
            'email': self.email,
            'source': 'CSV'
        }


class JSONUser(User):    
    def __init__(self, json_data: Dict[str, Any]):
        self.uid = json_data['uid']
        self.first_name = json_data['first_name']
        self.last_name = json_data['last_name']
        self.email = json_data['contacts']['email']
    
    def get_id(self) -> int:
        return self.uid
    
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def get_email(self) -> str:
        return self.email
    
    def get_info(self) -> Dict[str, str]:
        return {
            'id': str(self.uid),
            'full_name': self.get_full_name(),
            'email': self.email,
            'source': 'JSON'
        }


class RAWUser(User):
    def __init__(self, raw_line: str):
        parts = raw_line.strip().replace('<raw ', '').replace('>', '').split()
        self.last_name = parts[0]
        self.first_name = parts[1]
        self.email = parts[2]
        # Генерируем ID на основе хэша
        self.uid = abs(hash(f"{self.first_name}{self.last_name}{self.email}")) % 100000
    
    def get_id(self) -> int:
        return self.uid
    
    def get_full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def get_email(self) -> str:
        return self.email
    
    def get_info(self) -> Dict[str, str]:
        return {
            'id': str(self.uid),
            'full_name': self.get_full_name(),
            'email': self.email,
            'source': 'RAW'
        }


class UserCollection:    
    def __init__(self):
        self.users: List[User] = []
    
    def add_user(self, user: User) -> None:
        self.users.append(user)
    
    def add_users(self, users: List[User]) -> None:
        self.users.extend(users)
    
    def find_by_name(self, name: str) -> List[User]:
        return [u for u in self.users if name.lower() in u.get_full_name().lower()]
    
    def find_by_id(self, uid: int) -> User:
        for u in self.users:
            if u.get_id() == uid:
                return u
        return None
    
    def find_invalid_emails(self) -> List[User]:
        invalid = []
        for u in self.users:
            email = u.get_email()
            if '@' not in email or '.' not in email.split('@')[-1]:
                invalid.append(u)
        return invalid
    
    def get_all_emails(self) -> List[str]:
        """
        Получить все email-адреса из коллекции.
        
        Returns:
            list: Список всех email-адресов
        """
        return [u.get_email() for u in self.users]
    
    def get_valid_users(self) -> List[User]:
        """
        Получить всех пользователей с корректным email-адресом.
        
        Returns:
            list: Список пользователей с валидным email
        """
        return [u for u in self.users if '@' in u.get_email() and '.' in u.get_email()]
    
    def print_users(self) -> None:
        """Вывести всех пользователей в красивом формате"""
        print("\n=== Список пользователей ===")
        for u in self.users:
            info = u.get_info()
            print(f"« {info['full_name']} {info['email']}»")
    
    def print_statistics(self) -> None:
        """Вывести статистику по коллекции пользователей"""
        print(f"\nОтчёт о найденных/ненайденных пользователях, статистика валидности email-ов:")
        print(f"Всего пользователей: {len(self.users)}")
        valid = self.get_valid_users()
        invalid = self.find_invalid_emails()
        print(f"Корректные email: {len(valid)}")
        print(f"Некорректные email: {len(invalid)}")


if __name__ == "__main__":
    users_collection = UserCollection()
    csv_user1 = CSVUser("<csv 123;Иван Иванов;ivan@example.com>")
    csv_user2 = CSVUser("<csv 456;Петр Петров;petr@example.com>")
    
    json_user = JSONUser({
        "uid": 42, 
        "first_name": "Petr", 
        "last_name": "Petrov", 
        "contacts": {"email": "petr@example.com"}
    })
    
    raw_user = RAWUser("<raw Иванов Иван ivanov@example.com>")
    invalid_user = CSVUser("<csv 789;Иван Инвалид;invan.invalid>")
    
    users_collection.add_users([csv_user1, csv_user2, json_user, raw_user, invalid_user])
    print("=== ДЕМОНСТРАЦИЯ СИСТЕМЫ ===")
    
    users_collection.print_users()
    
    print("\n=== ОПЕРАЦИИ ===")
    
    # <emails> — вывести все email-адреса
    print("\n<emails> — вывести все email-адреса:")
    for email in users_collection.get_all_emails():
        print(f"  {email}")
    
    # <find name=Иван> — найти пользователей по имени
    print("\n<find name=Иван> — найти всех пользователей, в имени которых встречается «Иван»:")
    found = users_collection.find_by_name("Иван")
    for u in found:
        print(f"  « {u.get_full_name()} {u.get_email()}»")
    
    # <invalid> — показать некорректные email
    print("\n<invalid> — показать записи с некорректным email:")
    invalid = users_collection.find_invalid_emails()
    for u in invalid:
        print(f"  « {u.get_full_name()} {u.get_email()}»")
    
    # Статистика
    users_collection.print_statistics()
