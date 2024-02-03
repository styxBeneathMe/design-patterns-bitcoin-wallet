import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar

from bitcoinwallet.core.repository.entity import UserEntity
from bitcoinwallet.core.repository.repository_factory import (
    IRepositoryFactory,
    NullRepositoryFactory,
)
from bitcoinwallet.core.utils import ConsoleLogger, ILogger

TUserService = TypeVar("TUserService", bound="UserServiceBuilder")


class IUserService(ABC):
    @abstractmethod
    def create_user(self) -> str:
        pass


@dataclass
class UserService(IUserService):
    logger: ILogger
    repository_factory: IRepositoryFactory

    def create_user(self) -> str:
        self.logger.info("Creating new user")
        api_key = str(uuid.uuid4())
        user_entity = UserEntity(api_key=api_key, wallet_count=0)
        self.repository_factory.get_repository().save(user_entity)
        self.logger.info(f"Created user, api_key = {api_key}")
        return api_key


class UserServiceBuilder:
    def __init__(self) -> None:
        self.service = UserService(
            logger=ConsoleLogger(UserService.__name__),
            repository_factory=NullRepositoryFactory(),
        )

    def set_logger(self: TUserService, logger: ILogger) -> TUserService:
        self.service.logger = logger
        return self

    def set_repository_factory(
        self: TUserService, repository_factory: IRepositoryFactory
    ) -> TUserService:
        self.service.repository_factory = repository_factory
        return self

    def build(self) -> UserService:
        return self.service


class NullUserService(IUserService):
    def create_user(self) -> str:
        return "USER NOT CREATED"