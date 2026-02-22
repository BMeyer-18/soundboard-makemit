import argparse
from train_model import TrainModel
from gesture_classification import GestureClassifier

def main():
    args = get_args()
    if not args.model_path:
            raise ModuleNotFoundError("No path for model")
    if args.train:
        if not args.data_path:
            raise ModuleNotFoundError("No path for data")
        train(args)
    if args.use:
        use(args)
    
def get_args():
    parser = argparse.ArgumentParser(description="Train and run a custom MediaPipe gesture classification model.")
    parser.add_argument('-t', '--train', action="store_true", help="Train a custom model with specified training data.")
    parser.add_argument('-u', '--use', action="store_true", help="Use a trained model on live webcam data.")
    parser.add_argument('-d', '--data-path', type=str, nargs='?', help="Specify the path for the training data folder.")
    parser.add_argument('-m', '--model-path', type=str, nargs='?', help="Specify the path for the model file.")
    parser.print_help()

    return parser.parse_args()

def train(args):
    trainer = TrainModel(args.data_path, args.model_path)
    trainer.load_data(0.8)
    trainer.train_model()
    loss, acc = trainer.evaluate_performance
    print(f"accuracy: {acc}, loss: {loss}")

def use(args):
    classifier = GestureClassifier(args.model_path, 0.8)
    classifier.classify_live_footage(15)
    print("done")

if __name__ == "__main__":
    main()
