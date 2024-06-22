from dataclasses import dataclass, field


@dataclass
class Storage:
    user_storage: list = field(default_factory=list, init=False)