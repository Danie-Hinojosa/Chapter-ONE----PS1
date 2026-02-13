import cv2
import csv

VIDEO_PATH = 'video.mp4'
OUTPUT_CSV = 'coordinates.csv'

def track_video():
    cap = cv2.VideoCapture(VIDEO_PATH)
    results = []
    frame_count = 0

    print("Instrucciones:")
    print("- Haz clic en el animal para registrar su posición.")
    print("- Presiona cualquier tecla para pasar al siguiente frame.")
    print("- Presiona 'q' para guardar y salir.")

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            # Guardamos el frame y las coordenadas donde hiciste clic
            results.append([frame_count, x, y])
            print(f"Frame {frame_count}: Guardado x={x}, y={y}")
            # Dibujamos un círculo temporal para feedback
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Tracking Manual", frame)

    cv2.namedWindow("Tracking Manual")
    cv2.setMouseCallback("Tracking Manual", click_event)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        cv2.imshow("Tracking Manual", frame)
        
        # El programa se detiene en cada frame para que hagas clic
        # Presiona cualquier tecla (que no sea 'q') para avanzar al siguiente
        key = cv2.waitKey(0) & 0xFF
        if key == ord('q'):
            break

    # Guardar a CSV
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['frame#', 'xcoor', 'ycoor'])
        writer.writerows(results)

    cap.release()
    cv2.destroyAllWindows()
    print(f"Listo. Archivo {OUTPUT_CSV} generado con {len(results)} puntos.")

if __name__ == "__main__":
    track_video()