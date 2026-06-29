import argparse
import sys
from play_audio import PlayAudio
from training_files.gesture_classification import GestureClassifier

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

# Main function for the gesture recognition application
def get_args():
    parser = argparse.ArgumentParser(description="Train and run a custom MediaPipe gesture classification model.")
    parser.add_argument('-t', '--train', action="store_true", help="Train a custom model with specified training data.")
    parser.add_argument('-u', '--use', action="store_true", help="Use a trained model on live webcam data.")
    parser.add_argument('-d', '--data-path', type=str, nargs='?', help="Specify the path for the training data folder.")
    parser.add_argument('-m', '--model-path', type=str, nargs='?', help="Specify the path for the model file.")
    return parser.parse_args()

# Training class for gesture recognition
def train(args):
    from training_files.train_model import TrainModel
    trainer = TrainModel(args.data_path, args.model_path)
    trainer.load_data(0.8)
    trainer.train_model()
    loss, acc = trainer.evaluate_performance()
    print(f"accuracy: {acc}, loss: {loss}")

# Usage class for gesture recognition. Restarts the capture window if no gesture is detected.
def use(args):
    classifier = GestureClassifier(args.model_path, 0.3)

    while True:
        last_gesture = classifier.classify_live_footage(2)
        if last_gesture is None:
            print("Camera/frame error during capture window, retrying...")
            continue
        elif last_gesture == "none":
            print("No hand gesture detected. Shutting down.")
            sys.exit(0)
            # Does't work as intended
        else:
            print(f"Detected gesture: {last_gesture}")
        

if __name__ == "__main__":
    main()
