import argparse
import json
import os
import string
import uuid


def import_data(args):
    classes = ['chef', 'doctor', 'engineer', 'farmer', 'firefighter', 'judge', 'mechanic', 'pilot', 'police', 'waiter']
    choices = []
    class_to_answer_label = {}
    for class_label, answer_label in zip(classes, string.ascii_uppercase):
        choices.append({
            "label": answer_label,
            "text": class_label,
        })
        class_to_answer_label[class_label] = answer_label

    folder_path = os.path.abspath(os.path.expanduser(args.dir))
    output_path = os.path.abspath(os.path.expanduser(args.output))

    os.makedirs(output_path, exist_ok=True)
    train_filepath = os.path.join(output_path, 'train_rand_split.jsonl')
    dev_filepath = os.path.join(output_path, 'dev_rand_split.jsonl')
    test_filepath = os.path.join(output_path, 'test_rand_split_no_answers.jsonl')
    with open(train_filepath, 'w') as fout_train:
        with open(dev_filepath, 'w') as fout_dev:
            with open(test_filepath, 'w') as fout_test:

                i = 0
                max_i = 1e6
                print()
                for filename in os.listdir(folder_path):
                    if i >= max_i:
                        break

                    if not filename.endswith('_label.json'):
                        continue

                    filepath = os.path.join(folder_path, filename)
                    #print(filename)
                    print('\r', '{:06d}'.format(i + 1), sep='', end='')
                    with open(filepath) as f:
                        label_info = json.load(f)
                    gt_class = filename.split('-', 1)[0]
                    caption = label_info['caption']
                    #print(json.dumps(label_info, indent=2))
                    #print(caption)
                    #print(gt_class)

                    stem = 'There is ' + caption + '. What is the occupation of the person?'

                    jsonline = {
                        "answerKey": class_to_answer_label.get(gt_class, "A"),
                        "id": uuid.uuid4().hex,
                        "question": {
                            "question_concept": "people",
                            "choices": choices,
                            "stem": stem,
                        }
                    }
                    #jsonline["answerKey"] = class_to_answer_label.get(gt_class, "A")
                    json.dump(jsonline, fout_train)
                    fout_train.write('\n')
                    json.dump(jsonline, fout_dev)
                    fout_dev.write('\n')
                    del jsonline["answerKey"]
                    json.dump(jsonline, fout_test)
                    fout_test.write('\n')

                    i += 1
    print('\ndone')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', default='~/SceneGraphGenZeroShotWithGSAM/outputs/sgg_2661/', help="directory to import data from")
    parser.add_argument('--output', default='./data/custom/', help="directory to import data from")
    args = parser.parse_args()
    import_data(args)


if __name__ == '__main__':
    main()

