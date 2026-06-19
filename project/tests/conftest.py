import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from fastapi.testclient import TestClient

from src.service.app import app
from src.config import MODEL_PATH, ENCODERS_PATH, CATEGORICAL_COLS


@pytest.fixture
def client():
    """FastAPI тестовый клиент с корректной инициализацией"""
    # Используем контекстный менеджер для вызова lifespan
    with TestClient(app) as client:
        yield client


@pytest.fixture
def sample_normal_flow():
    """Пример нормального сетевого потока"""
    return {
        "dur": 0.000011,
        "proto": "udp",
        "service": "-",
        "state": "INT",
        "spkts": 2,
        "dpkts": 0,
        "sbytes": 496,
        "dbytes": 0,
        "rate": 90909.0902,
        "sttl": 254,
        "dttl": 0,
        "sload": 178571.4286,
        "dload": 0,
        "sloss": 0,
        "dloss": 0,
        "sinpkt": 0.011,
        "dinpkt": 0,
        "sjit": 0,
        "djit": 0,
        "swin": 0,
        "stcpb": 0,
        "dtcpb": 0,
        "dwin": 0,
        "tcprtt": 0,
        "synack": 0,
        "ackdat": 0,
        "smean": 248,
        "dmean": 0,
        "trans_depth": 0,
        "response_body_len": 0,
        "ct_srv_src": 1,
        "ct_state_ttl": 1,
        "ct_dst_ltm": 2,
        "ct_src_dport_ltm": 1,
        "ct_dst_sport_ltm": 1,
        "ct_dst_src_ltm": 2,
        "is_ftp_login": 0,
        "ct_ftp_cmd": 0,
        "ct_flw_http_mthd": 0,
        "ct_src_ltm": 1,
        "ct_srv_dst": 2,
        "is_sm_ips_ports": 0
    }


@pytest.fixture
def sample_attack_flow():
    """Пример аномального сетевого потока (DoS-атака)"""
    return {
        "dur": 0.000001,
        "proto": "tcp",
        "service": "http",
        "state": "CON",
        "spkts": 1000,
        "dpkts": 0,
        "sbytes": 500000,
        "dbytes": 0,
        "rate": 999999.9999,
        "sttl": 255,
        "dttl": 0,
        "sload": 999999.9999,
        "dload": 0,
        "sloss": 0,
        "dloss": 0,
        "sinpkt": 0.001,
        "dinpkt": 0,
        "sjit": 0,
        "djit": 0,
        "swin": 0,
        "stcpb": 0,
        "dtcpb": 0,
        "dwin": 0,
        "tcprtt": 0,
        "synack": 0,
        "ackdat": 0,
        "smean": 500,
        "dmean": 0,
        "trans_depth": 1,
        "response_body_len": 0,
        "ct_srv_src": 100,
        "ct_state_ttl": 100,
        "ct_dst_ltm": 100,
        "ct_src_dport_ltm": 100,
        "ct_dst_sport_ltm": 100,
        "ct_dst_src_ltm": 100,
        "is_ftp_login": 0,
        "ct_ftp_cmd": 0,
        "ct_flw_http_mthd": 0,
        "ct_src_ltm": 100,
        "ct_srv_dst": 100,
        "is_sm_ips_ports": 0
    }


@pytest.fixture
def sample_dataframe():
    """Пример DataFrame с данными"""
    data = {
        'dur': [0.000011, 0.000001],
        'proto': ['udp', 'tcp'],
        'service': ['-', 'http'],
        'state': ['INT', 'CON'],
        'spkts': [2, 1000],
        'dpkts': [0, 0],
        'sbytes': [496, 500000],
        'dbytes': [0, 0],
        'rate': [90909.0902, 999999.9999],
        'sttl': [254, 255],
        'dttl': [0, 0],
        'sload': [178571.4286, 999999.9999],
        'dload': [0, 0],
        'sloss': [0, 0],
        'dloss': [0, 0],
        'sinpkt': [0.011, 0.001],
        'dinpkt': [0, 0],
        'sjit': [0, 0],
        'djit': [0, 0],
        'swin': [0, 0],
        'stcpb': [0, 0],
        'dtcpb': [0, 0],
        'dwin': [0, 0],
        'tcprtt': [0, 0],
        'synack': [0, 0],
        'ackdat': [0, 0],
        'smean': [248, 500],
        'dmean': [0, 0],
        'trans_depth': [0, 1],
        'response_body_len': [0, 0],
        'ct_srv_src': [1, 100],
        'ct_state_ttl': [1, 100],
        'ct_dst_ltm': [2, 100],
        'ct_src_dport_ltm': [1, 100],
        'ct_dst_sport_ltm': [1, 100],
        'ct_dst_src_ltm': [2, 100],
        'is_ftp_login': [0, 0],
        'ct_ftp_cmd': [0, 0],
        'ct_flw_http_mthd': [0, 0],
        'ct_src_ltm': [1, 100],
        'ct_srv_dst': [2, 100],
        'is_sm_ips_ports': [0, 0]
    }
    return pd.DataFrame(data)