document.addEventListener("DOMContentLoaded", function () {
  const likeButtons = document.querySelectorAll(".like-button");

  likeButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const imageId = button.getAttribute("data-image-id");
      const isLiked = button.classList.contains("liked"); // ✅ liked 여부 확인

      const url = isLiked ? `/image/${imageId}/dislike` : `/image/${imageId}/like`; // ✅ 요청 URL 결정

      fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ like: !isLiked }), // ✅ true -> false, false -> true
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            button.classList.toggle("liked"); // ✅ 좋아요 상태 변경
            button.style.color = button.classList.contains("liked") ? "red" : "white"; // ✅ 색상 변경
          }
        })
        .catch((error) => console.error("Error", error));
    });
  });
});
document.getElementById("searchForm").addEventListener("submit", function (event) {
  event.preventDefault(); // ✅ 기본 폼 제출 방지
  const searchValue = document.getElementById("searchInput").value.trim(); // ✅ 입력 값 가져오기

  if (searchValue) {
    window.location.href = `/search/${encodeURIComponent(searchValue)}`; // ✅ 동적 URL 변경
  }
});
document.addEventListener("DOMContentLoaded", function () {
  console.log("JavaScript Loaded!");

  /*** ✅ 업로드 모달 관리 ***/
  let uploadModal = document.getElementById("uploadModal");
  let openUploadModalBtn = document.getElementById("openUploadModal");
  let closeUploadModalBtn = document.getElementById("closeUploadModal");

  if (uploadModal && openUploadModalBtn && closeUploadModalBtn) {
    openUploadModalBtn.addEventListener("click", function () {
      uploadModal.style.display = "block";
      console.log("Opening upload modal");
    });

    closeUploadModalBtn.addEventListener("click", function () {
      uploadModal.style.display = "none";
      console.log("Closing upload modal");
    });

    window.addEventListener("click", function (event) {
      if (event.target === uploadModal) {
        uploadModal.style.display = "none";
        console.log("Clicked outside upload modal, closing");
      }
    });
  }

  /*** ✅ 삭제 모달 관리 ***/
  let deleteModal = document.getElementById("deleteModal");
  let closeDeleteModalBtn = document.getElementById("closeDeleteModal");
  let deletePasswordInput = document.getElementById("deletePassword");
  let confirmDeleteBtn = document.getElementById("confirmDelete");
  let selectedImageId = null;

  document.querySelectorAll(".delete-button").forEach((button) => {
    button.addEventListener("click", function () {
      let parentCell = this.closest(".cell");
      if (!parentCell) {
        console.error("Error: .cell not found!");
        return;
      }

      let imageElement = parentCell.querySelector("img");
      if (!imageElement) {
        console.error("Error: Image element not found in .cell!");
        return;
      }

      selectedImageId = imageElement.getAttribute("alt");
      console.log(`Opening delete modal for image: ${selectedImageId}`);

      deleteModal.style.display = "block"; // ✅ 삭제 모달 열기
    });
  });

  if (closeDeleteModalBtn) {
    closeDeleteModalBtn.addEventListener("click", function () {
      deleteModal.style.display = "none";
      deletePasswordInput.value = ""; // ✅ 입력 필드 초기화
      console.log("Closing delete modal");
    });

    window.addEventListener("click", function (event) {
      if (event.target === deleteModal) {
        deleteModal.style.display = "none";
        deletePasswordInput.value = "";
        console.log("Clicked outside delete modal, closing");
      }
    });
  }

  confirmDeleteBtn.addEventListener("click", function () {
    let password = deletePasswordInput.value.trim();
    if (!password) {
      alert("비밀번호를 입력하세요!");
      return;
    }

    console.log(`Sending delete request for ${selectedImageId} with password ${password}`);

    fetch(`/image/${selectedImageId}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ password: password }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          console.log("Image deleted successfully!");
          location.reload();
        } else {
          alert(data.error);
        }
      })
      .catch((error) => console.error("Error:", error));
  });

  // ✅ 파일 선택 시 파일명 표시
  const fileInput = document.getElementById("fileInput");
  const fileNameDisplay = document.getElementById("fileName");
  if (fileInput && fileNameDisplay) {
    fileInput.addEventListener("change", function () {
      fileNameDisplay.textContent = fileInput.files.length > 0 ? fileInput.files[0].name : "선택된 파일 없음";
    });
  }
});
