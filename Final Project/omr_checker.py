import cv2
import numpy as np
from answer_key import ANSWER_KEY

def process_omr(image_path):
    # Load image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours of the bubbles
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bubble_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 50]  # Filter small noise

    # Sort contours top-to-bottom, left-to-right
    bubble_contours = sorted(bubble_contours, key=lambda c: cv2.boundingRect(c)[1] * 1000 + cv2.boundingRect(c)[0])

    # Divide into rows
    rows = [bubble_contours[i:i+5] for i in range(0, len(bubble_contours), 5)]
    marked_answers = []

    # Check the darkest bubble in each row
    for row in rows:
        darkness = [cv2.countNonZero(cv2.bitwise_and(thresh, thresh, mask=cv2.drawContours(np.zeros_like(thresh), [cnt], -1, 255, -1))) for cnt in row]
        marked_index = np.argmax(darkness)
        marked_answers.append(marked_index)

    # Compare with answer key
    score = sum([1 for i, ans in enumerate(ANSWER_KEY) if ans == marked_answers[i]])
    total_questions = len(ANSWER_KEY)

    # Return results
    return {"score": score, "total": total_questions, "answers": marked_answers}

# Example test
if __name__ == "__main__":
    results = process_omr("uploads/3.jpg")  # Replace with your image path
    print("Result:", results)
