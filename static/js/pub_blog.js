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

        if (!title || !content) {
            alert("标题和内容不能为空！");
            return;
        }

        let formData = new FormData();
        formData.append("title", title);
        formData.append("category", category);
        formData.append("content", content);
        formData.append("csrfmiddlewaretoken", csrfmiddlewaretoken);
        if (cover) {
            formData.append("cover", cover);
        }

        console.log("📤 Sending AJAX request with data:", { title, category, cover });

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