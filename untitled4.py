from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Gizli görüntüyü ana görüntüye gömme
def embed_image(main_image_path, secret_image_path, output_image_path):
    main_image = Image.open(main_image_path).convert("RGB")
    secret_image = Image.open(secret_image_path).convert("RGB")
    secret_image = secret_image.resize(main_image.size)
    
    main_data = np.array(main_image)
    secret_data = np.array(secret_image)
    
    # Gömme işlemi
    encoded_data = main_data.copy()
    encoded_data[:, :, 0] = (main_data[:, :, 0] & 0xFE) | (secret_data[:, :, 0] >> 7)
    encoded_data[:, :, 1] = (main_data[:, :, 1] & 0xFE) | (secret_data[:, :, 1] >> 7)
    encoded_data[:, :, 2] = (main_data[:, :, 2] & 0xFE) | (secret_data[:, :, 2] >> 7)
    
    encoded_image = Image.fromarray(encoded_data)
    encoded_image.save(output_image_path)
    
    # Görselleştirme
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.title("Ana Görüntü")
    plt.imshow(main_image)
    plt.axis("off")
    
    plt.subplot(1, 2, 2)
    plt.title("Gömülü Görüntü")
    plt.imshow(encoded_image)
    plt.axis("off")
    
    plt.tight_layout()
    plt.show()
    
    print(f"Gizli görüntü '{output_image_path}' dosyasına başarıyla gömüldü.")

# Gizli görüntüyü çıkarma
def extract_image(stego_image_path, output_image_path, password):
    correct_password = "I am better"
    if password != correct_password:
        print("Hatalı şifre!")
        return
    
    stego_image = Image.open(stego_image_path).convert("RGB")
    stego_data = np.array(stego_image)
    
    # Çıkarma işlemi
    secret_data = np.zeros_like(stego_data)
    secret_data[:, :, 0] = (stego_data[:, :, 0] & 1) << 7
    secret_data[:, :, 1] = (stego_data[:, :, 1] & 1) << 7
    secret_data[:, :, 2] = (stego_data[:, :, 2] & 1) << 7
    
    secret_data = secret_data.astype('uint8')
    secret_image = Image.fromarray(secret_data, mode="RGB")
    secret_image.save(output_image_path)
    
    # Görselleştirme
    plt.figure(figsize=(8, 4))
    
    plt.subplot(1, 2, 2)
    plt.title("Çıkarılan Gizli Görüntü")
    plt.imshow(secret_image)
    plt.axis("off")
    
    plt.tight_layout()
    plt.show()
    
    print(f"Gizli görüntü '{output_image_path}' dosyasına başarıyla çıkarıldı.")

# Kullanım
main_image_path = "C:/Users/Kerem/Desktop/Sayısal Proje/main_image.png"  # Ana görüntü
secret_image_path = "C:/Users/Kerem/Desktop/Sayısal Proje/secret_image.png"  # Gizli görüntü
output_image_path = "C:/Users/Kerem/Desktop/Sayısal Proje/stego_image.png"  # Gömülü görüntü
extracted_image_path = "C:/Users/Kerem/Desktop/Sayısal Proje/extracted_image.png"  # Çıkarılan görüntü

embed_image(main_image_path, secret_image_path, output_image_path)

password = input("Şifreyi girin: ")
extract_image(output_image_path, extracted_image_path, password)
