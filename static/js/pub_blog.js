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

    $("#submit-btn").click(function (event) {
        console.log("🔵 Submit button clicked");
        //阻止按钮的默认行为
        event.preventDefault();

        let title = $("input[name='title']").val();
        let category = $("#category-select").val();
        let content = easyMDE.value(); // Get content from EasyMDE
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();

        if (!title || !content) {
            alert("标题和内容不能为空！");
            return;
        }

        console.log("📤 Sending AJAX request with data:", { title, category });

        $.ajax('/blog/pub', {
            method: 'POST',
            data: { title, category, content, csrfmiddlewaretoken },
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