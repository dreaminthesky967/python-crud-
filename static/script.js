document.addEventListener("DOMContentLoaded", function () {
    // Modal Tambah
    const modalTambah = document.getElementById("modal");
    const openTambah = document.getElementById("openModal");
    const closeTambah = modalTambah?.querySelector(".close");

    if (modalTambah && openTambah && closeTambah) {
        openTambah.addEventListener("click", () => {
            modalTambah.style.display = "flex";
        });

        closeTambah.addEventListener("click", () => {
            modalTambah.style.display = "none";
        });

        window.addEventListener("click", (event) => {
            if (event.target === modalTambah) {
                modalTambah.style.display = "none";
            }
        });
    }

    // Notifikasi
    function showNotif(pesan, tipe = "success") {
        const notif = document.getElementById("notif");
        notif.textContent = pesan;

        // Tambahkan kelas berdasarkan tipe notifikasi
        notif.className = `notif show ${tipe}`;

        setTimeout(() => {
            notif.className = "notif";
        }, 3000); // 3 detik
    }

    // Modal Edit
    const modalEdit = document.getElementById("modalEdit");
    const closeEdit = document.getElementById("closeEdit");

    if (modalEdit && closeEdit) {
        document.querySelectorAll(".btn-edit").forEach(button => {
            button.addEventListener("click", function () {
                const id = this.getAttribute("data-id");
                const name = this.getAttribute("data-name");
                const description = this.getAttribute("data-description");
                const price = this.getAttribute("data-price");

                document.getElementById("editId").value = id;
                document.getElementById("editNamaProduk").value = name;
                document.getElementById("editDeskripsiProduk").value = description;
                document.getElementById("editHargaProduk").value = price;

                document.getElementById("editForm").action = `/edit/${id}`;

                modalEdit.style.display = "flex";
            });
        });

        closeEdit.addEventListener("click", () => {
            modalEdit.style.display = "none";
        });

        window.addEventListener("click", (event) => {
            if (event.target === modalEdit) {
                modalEdit.style.display = "none";
            }
        });
    }

    // Pencarian Produk
    const searchInput = document.getElementById("search");
    const tableRows = document.querySelectorAll("#productTable tbody tr");

    if (searchInput) {
        searchInput.addEventListener("keyup", function () {
            const searchTerm = searchInput.value.toLowerCase();

            tableRows.forEach(row => {
                const productName = row.querySelector(".nama-produk").textContent.toLowerCase();
                const productDesc = row.querySelector(".deskripsi-produk").textContent.toLowerCase();

                const match = productName.includes(searchTerm) || productDesc.includes(searchTerm);
                row.style.display = match ? "" : "none";
            });
        });
    }

    // Menampilkan Notifikasi
    const urlParams = new URLSearchParams(window.location.search);
    const msg = urlParams.get("msg");
    const type = urlParams.get("type");

    if (msg) {
        showNotif(msg, type || "success");
    }

    // Menghapus Produk
    document.querySelectorAll(".btn-delete").forEach(button => {
        button.addEventListener("click", function () {
            const row = this.closest("tr");
            const id = this.getAttribute("data-id"); 

            if (confirm("Yakin ingin menghapus produk ini?")) {
                fetch(`/delete/${id}`, {
                    method: "POST",  
                    headers: {
                        "Content-Type": "application/json"
                    }
                }).then(response => {
                    if (response.ok) {
                        row.remove(); 
                        alert("Produk berhasil dihapus!");
                    } else {
                        alert("Gagal menghapus produk.");
                    }
                }).catch(error => {
                    alert("Terjadi kesalahan: " + error.message);  
                });
            }
        });
    });
});
