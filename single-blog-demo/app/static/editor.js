/*
 * editor.js
 *
 * 负责 Quill 富文本编辑器初始化。
 *
 * 重点流程：
 * 1. 用户在 Quill 里编辑正文；
 * 2. 用户选择图片时，JS 上传图片到 /admin/uploads/image；
 * 3. 后端返回图片地址；
 * 4. JS 把图片地址插入 Quill；
 * 5. 表单提交前，把 Quill 里的 HTML 写入隐藏 input。
 */

const editorElement = document.querySelector("#editor");
const formElement = document.querySelector("#article-form");
const contentInput = document.querySelector("#content-input");

if (editorElement && formElement && contentInput) {
  const quill = new Quill("#editor", {
    theme: "snow",
    placeholder: "请输入文章正文，可以插入图片...",
    modules: {
      toolbar: {
        container: [
          [{ header: [1, 2, 3, false] }],
          ["bold", "italic", "underline"],
          [{ list: "ordered" }, { list: "bullet" }],
          ["link", "image"],
          ["clean"],
        ],
        handlers: {
          image: uploadImage,
        },
      },
    },
  });

  function uploadImage() {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = "image/*";
    input.click();

    input.onchange = async () => {
      const file = input.files[0];
      if (!file) {
        return;
      }

      const formData = new FormData();
      formData.append("image", file);

      const response = await fetch("/admin/uploads/image", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        alert("图片上传失败，请确认已经登录后台。");
        return;
      }

      const data = await response.json();
      const range = quill.getSelection(true);
      quill.insertEmbed(range.index, "image", data.url);
      quill.setSelection(range.index + 1);
    };
  }

  formElement.addEventListener("submit", () => {
    // Quill 的 root.innerHTML 就是正文 HTML。
    contentInput.value = quill.root.innerHTML;
  });
}
