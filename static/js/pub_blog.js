$(function () {
    console.log("✅ pub_blog.js loaded and ready");

    // Initialize EasyMDE
    const easyMDE = new EasyMDE({
        element: document.getElementById('markdown-editor'),
        placeholder: "在此处编写您的博客内容 (支持 Markdown)...",
        spellChecker: false,
        status: false,
        autosave: {
            enabled: true,
            uniqueId: "pub_blog_content",
            delay: 1000,
        },
    });

    console.log("✅ EasyMDE initialized");

    // Emoji Picker Logic
    const emojiBtn = document.createElement('button');
    emojiBtn.className = 'emoji-btn';
    emojiBtn.type = 'button';
    emojiBtn.innerHTML = '<i class="bi bi-emoji-smile"></i>';
    emojiBtn.title = 'Insert Emoji';
    // Style to match EasyMDE toolbar
    emojiBtn.style.cssText = 'background:transparent;border:none;cursor:pointer;font-size:16px;padding:0 10px;color:#2c3e50;outline:none;line-height:1.5;';

    // Add hover effect
    emojiBtn.onmouseover = () => emojiBtn.style.color = '#3b82f6';
    emojiBtn.onmouseout = () => emojiBtn.style.color = '#2c3e50';

    const toolbar = document.querySelector('.editor-toolbar');
    if (toolbar) {
        toolbar.appendChild(emojiBtn);
    }

    const emojiPopup = document.getElementById('emoji-popup');
    if (emojiPopup) {
        document.body.appendChild(emojiPopup);
    }
    const picker = document.querySelector('emoji-picker');

    if (emojiBtn && emojiPopup && picker) {
        emojiBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            if (emojiPopup.style.display === 'block') {
                emojiPopup.style.display = 'none';
            } else {
                const rect = emojiBtn.getBoundingClientRect();
                emojiPopup.style.top = (window.scrollY + rect.bottom + 5) + 'px';
                // Adjust if flows off screen
                let left = window.scrollX + rect.left;
                if (left + 350 > window.innerWidth) {
                    left = window.innerWidth - 360;
                }
                emojiPopup.style.left = left + 'px';
                emojiPopup.style.display = 'block';
            }
        });

        document.addEventListener('click', (e) => {
            if (!emojiPopup.contains(e.target) && e.target !== emojiBtn) {
                emojiPopup.style.display = 'none';
            }
        });

        picker.addEventListener('emoji-click', event => {
            const emoji = event.detail.unicode;
            const doc = easyMDE.codemirror.getDoc();
            const cursor = doc.getCursor();
            doc.replaceRange(emoji, cursor);
            emojiPopup.style.display = 'none';
            easyMDE.codemirror.focus();
        });
    }

    // Handle file upload
    $("#markdown-upload").change(function (e) {
        const file = e.target.files[0];
        if (!file) return;

        // Check file extension
        if (!file.name.endsWith('.md')) {
            alert('请上传 .md 格式的文件');
            this.value = ''; // Clear input
            return;
        }

        const reader = new FileReader();
        reader.onload = function (e) {
            const content = e.target.result;
            easyMDE.value(content);
            console.log("📄 Markdown file loaded");
        };
        reader.onerror = function (e) {
            console.error("❌ Error reading file:", e);
            alert('读取文件失败');
        };
        reader.readAsText(file);
    });

    $("#submit-btn").click(function (event) {
        console.log("🔵 Submit button clicked");
        //阻止按钮的默认行为
        event.preventDefault();

        let title = $("input[name='title']").val();
        let category = $("#category-select").val();
        let content = easyMDE.value(); // Get content from EasyMDE
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
        let cover = $("input[name='cover']")[0].files[0];
        let tags = $("#tags").val();

        if (!title || !content) {
            alert("标题和内容不能为空！");
            return;
        }

        let formData = new FormData();
        formData.append("title", title);
        formData.append("category", category);
        formData.append("content", content);
        formData.append("tags", tags);
        formData.append("csrfmiddlewaretoken", csrfmiddlewaretoken);
        if (cover) {
            formData.append("cover", cover);
        }

        console.log("📤 Sending AJAX request with data:", { title, category, cover, tags });

        $.ajax('/blog/pub', {
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function (result) {
                console.log("✅ AJAX Success response:", result);
                if (result['code'] === 200) {
                    // Clear autosave
                    easyMDE.clearAutosavedValue();

                    //跳转到博客详情
                    let blog_id = result['data']['blog_id'];
                    let targetUrl = "/blog/detail/" + blog_id;
                    console.log("🔄 Redirecting to:", targetUrl);
                    //获取博客id
                    window.location.href = targetUrl;
                } else {
                    console.warn("⚠️ Server returned non-200 code:", result);
                    alert(result['message']);
                }
            },
            error: function (xhr, status, error) {
                console.error("❌ AJAX Error:", { xhr, status, error });
                console.error("Response text:", xhr.responseText);
                alert("发布失败: " + error)
            }
        })

    })
})