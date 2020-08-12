import torch

from dataset import MiniImageNetDataLoader
from model import PrototypicalNetwork
from paths import EMBEDDING_PATH
from tester import Tester


def main(dataset: str, n: int, n_s: int, n_q: int, testsize: int, device: str = 'cpu'):
    assert device == 'cpu' or 'cuda' in device
    assert dataset in ['miniimagenet', 'omniglot']
    assert EMBEDDING_PATH.exists()
    model = PrototypicalNetwork()
    model.load_state_dict(torch.load(EMBEDDING_PATH, device))
    print('Loaded trained model')
    if dataset == 'miniimagenet':
        data = MiniImageNetDataLoader(1, 5, 5, n, n_s, n_q, -1, -1, testsize, device)
    else:
        raise NotImplementedError("Omniglot not implemented")
    tester = Tester(model, torch.nn.CrossEntropyLoss(), device)

    tester.test(data.test_dataloader(), testsize)