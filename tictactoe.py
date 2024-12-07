from flask import Flask, request, render_template

app = Flask(__name__)

# Posisi papan
# 1 2 3
# 4 5 6
# 7 8 9

GARIS_KEMENANGAN = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],  # Horizontal
    [1, 4, 7],
    [2, 5, 8],
    [3, 6, 9],  # Vertikal
    [1, 5, 9],
    [3, 5, 7],  # Diagonal
]

papan = [0] * 9
pemain_sekarang = 1  # Pemain 1 mulai

def langkah_tersedia():
    return [i + 1 for i, e in enumerate(papan) if e == 0]

def mainkan_langkah(langkah):
    global pemain_sekarang
    langkah = int(langkah) - 1
    if papan[langkah] == 0:
        papan[langkah] = pemain_sekarang
        pemain_sekarang = 3 - pemain_sekarang  # Ganti antara 1 dan 2.

def kalah(siapapun):
    """Periksa apakah pemain yang diberikan telah menang."""
    return any(all(papan[c - 1] == siapapun for c in garis) for garis in GARIS_KEMENANGAN)

def sudah_selesai():
    return not langkah_tersedia() or kalah(1) or kalah(2)

def string_spot(i, j):
    return ["_", "O", "X"][papan[3 * j + i]]

def pemenang():
    if kalah(1):
        return "Pemain O Menang!"
    if kalah(2):
        return "Pemain X Menang!"
    return "Seri!"

@app.route("/", methods=["GET", "POST"])
def mainkan_permainan():
    global papan, pemain_sekarang

    # Menangani pengiriman form.
    if "pilihan" in request.form and not sudah_selesai():
        mainkan_langkah(request.form["pilihan"])
    if "reset" in request.form:
        papan = [0 for _ in range(9)]
        pemain_sekarang = 1

    # Menentukan pesan status permainan.
    if sudah_selesai():
        pesan = pemenang()
    else:
        pesan = f"Pemain {'O' if pemain_sekarang == 1 else 'X'}, giliranmu!"

    # Render template tanpa memperbarui cookie
    return render_template('index.html', pesan=pesan, string_spot=string_spot)

if __name__ == "__main__":
    app.run(debug=True)
