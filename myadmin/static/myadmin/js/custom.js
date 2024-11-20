const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
const elBulkDeleteButton = document.getElementById('bulk-delete');
const checkboxes = document.querySelectorAll('tbody input[type="checkbox"]');
const elSearch = document.getElementById('category-search');
const elClearSearch = document.getElementById('clear-search');
const elImageInput = document.getElementById("imageInput")
const elNewImagePreview = document.getElementById("newImagePreview")
const elOldImagePreview = document.getElementById("oldImagePreview")
if (elBulkDeleteButton) bulkDelete();

// delete
function deleteItem(itemType, itemId) {
    Swal.fire({
      title: "Bạn có muốn xoá danh mục này không?",
      showCancelButton: true,
      confirmButtonText: "Có",
      cancelButtonText: "Không",
    }).then((result) => {
      if (result.isConfirmed) {
        fetch(`/myadmin/delete/${itemType}/${itemId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                Swal.fire("Xoá thành công!", data.message, "success")
                .then(() => {
                        location.reload();
                    }
                );
//                Swal.fire({
//                        title: "Xoá thành công!",
//                        text: data.message,
//                        icon: "success"
//                    }).then(() => {
//                        location.reload();
//                    });
            } else {
                Swal.fire("Có lỗi xảy ra!", data.message, "error");
            }
        })
        .catch(error => {
            Swal.fire("Có lỗi xảy ra!", "Không thể kết nối tới server.", "error");
        });
      } else {
        Swal.fire("Không xoá", "", "info");
      }
    });
}

// Cập nhật lại nút Bulk Delete khi lọc, search
function disabled_and_count() {
    if (elBulkDeleteButton) {
        const selectedCategories = Array.from(document.querySelectorAll('tbody input[type="checkbox"]:checked'));
        elBulkDeleteButton.disabled = selectedCategories.length === 0;
        elBulkDeleteButton.textContent = `Bulk Delete (${selectedCategories.length})`;
    }
}

// Tô màu
function initCheckboxChangeEvent(){
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const row = this.closest('tr');
            checkbox.checked ? row.classList.add('selected') : row.classList.remove('selected');
            disabled_and_count();
        });
    });
}

// Bulk Delete
function bulkDelete() {
    initCheckboxChangeEvent();

    document.getElementById('checkAll').addEventListener('change', function () {
        const isChecked = this.checked;
        document.querySelectorAll('tbody input[type="checkbox"]').forEach((rowCheckbox) => {
            rowCheckbox.checked = isChecked;
            var event = new Event('change');
            rowCheckbox.dispatchEvent(event);
        });
    });
    const itemType = elBulkDeleteButton.dataset.type
    elBulkDeleteButton.addEventListener('click', function () {
        const selectedItems = Array.from(document.querySelectorAll('tbody input[type="checkbox"]:checked')).map(
            (checkbox) => checkbox.value
        );

        if (selectedItems.length === 0) {
            alert('No categories selected for deletion.');
            return;
        }

        Swal.fire({
            title: 'Bạn có muốn xoá danh mục này không?',
            showCancelButton: true,
            confirmButtonText: 'Có',
            cancelButtonText: 'Không',
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`/myadmin/bulk-delete/${itemType}`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ item_ids: selectedItems }),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            Swal.fire('Xoá thành công!', data.message, 'success').then(() => {
                                location.reload();
                            });
                        } else {
                            Swal.fire('Có lỗi xảy ra!', data.message, 'error');
                        }
                    })
                    .catch((error) => {
                        Swal.fire('Có lỗi xảy ra!', 'Không thể kết nối tới server.', 'error');
                    });
            } else {
                Swal.fire('Không xoá', '', 'info');
            }
        });
    });
}



let slugDirty = false;

function setSlugDirty(isDirty) {
    slugDirty = isDirty;
}

function updateSlug(name) {
    if (!slugDirty) {
        const slug = slugify(name, {
            lower: true,
            strict: true
        });
        document.getElementById('slugInput').value = slug;
    }
}

function updateSlugFromButton() {
    const name = document.querySelector('input[name="name"]').value;
    const slug = slugify(name, {
            lower: true,
            strict: true
        });
        document.getElementById('slugInput').value = slug;
}







// Lọc theo status
document.addEventListener('DOMContentLoaded', function() {

    // Kiểm tra tham số 'status' trong URL
    console.log(window.location.pathname + window.location.search)
    const Params = new URLSearchParams(window.location.search);
    const statusFromUrl = Params.get('status');
    var filterStatus = '';

    // Lắng nghe sự kiện click cho các nút
    document.querySelectorAll('.filter-status').forEach(button => {
        button.addEventListener('click', function(event) {

//            document.querySelectorAll('.filter-status').forEach(btn => {
//                btn.classList.remove('btn-primary');
//            });
//            this.classList.add('btn-primary');

            const filterStatus = button.dataset.value;
            Params.set('status', filterStatus);
            Params.set('page', '1')
            const newUrl = `${window.location.pathname}?${Params.toString()}`;
            window.location.href = newUrl;
        });
    });

    function FETCH(){
        fetch(window.location.pathname + window.location.search)
                    .then(response => response.text())
                    .then(html => {
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');
                        const newTable = doc.querySelector('.table-responsive');
                        document.querySelector('.table-responsive').innerHTML = newTable.innerHTML;
                        bulkDelete();
            });
    }
    function filterItems(status) {
        fetch(`/myadmin/category/filter?status=${status}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    filterStatus: filterStatus
                })
            })
            .then(response => response.json())
            .then(data => {
//                console.log('filterStatus: ', filterStatus)
                const tableBody = document.querySelector('tbody');
                tableBody.innerHTML = '';

                data.items.forEach(item => {
                    var row = /*html*/ `
                        <tr class="">
                            <td>
                                <input class="form-check-input" type="checkbox" value="38">
                            </td>
                            <td>${item.name}</td>
                            <td>${item.slug}</td>
                    `;

                    if (item.is_homepage) {
                        row += /*html*/ `
                            <td>
                                <span class="badge bg-success text-success-fg">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                         viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                         stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                         class="icon icon-tabler icon-tabler-check">
                                        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                                        <path d="M5 12l5 5l10 -10"></path>
                                    </svg>
                                </span>
                            </td>
                        `;
                    } else {
                        row += `
                            <td>
                                <span class="badge bg-danger text-danger-fg">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                         viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                         stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                                         class="icon icon-tabler icon-tabler-x">
                                        <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                                        <path d="M18 6l-12 12"></path>
                                        <path d="M6 6l12 12"></path>
                                    </svg>
                                </span>
                            </td>
                        `;
                    }

                    let statusClass, statusText;

                    if (item.status === 'published') {
                        statusClass = 'bg-success text-success-fg';
                        statusText = 'Published';
                    } else if (item.status === 'draft') {
                        statusClass = 'bg-secondary text-secondary-fg';
                        statusText = 'Draft';
                    } else {
                        statusClass = 'bg-warning text-warning-fg';
                        statusText = 'Pending';
                    }

                    row += `
                        <td>
                            <span class="badge ${statusClass}">${statusText}</span>
                        </td>
                    `;
                    row += `
                        <td>${item.layout}</td>
                        <td class="d-flex gap-1">
                            <a href="${item.edit_url}"
                               class="btn btn-sm btn-icon btn-primary">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                     viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                     stroke-linecap="round" stroke-linejoin="round"
                                     class="icon icon-tabler icons-tabler-outline icon-tabler-edit">
                                    <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                                    <path d="M7 7h-1a2 2 0 0 0 -2 2v9a2 2 0 0 0 2 2h9a2 2 0 0 0 2 -2v-1"></path>
                                    <path d="M20.385 6.585a2.1 2.1 0 0 0 -2.97 -2.97l-8.415 8.385v3h3l8.385 -8.415z"></path>
                                    <path d="M16 5l3 3"></path>
                                </svg>
                            </a>
                            <button type="button" class="btn btn-sm btn-icon btn-danger"
                                    onclick="deleteCategory('${item.id}')">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24"
                                     viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
                                     stroke-linecap="round" stroke-linejoin="round"
                                     class="icon icon-tabler icons-tabler-outline icon-tabler-trash">
                                    <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                                    <path d="M4 7l16 0"></path>
                                    <path d="M10 11l0 6"></path>
                                    <path d="M14 11l0 6"></path>
                                    <path d="M5 7l1 12a2 2 0 0 0 2 2h8a2 2 0 0 0 2 -2l1 -12"></path>
                                    <path d="M9 7v-3a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v3"></path>
                                </svg>
                            </button>
                        </td>
                    `;
                    row += `</tr>`;
                    tableBody.innerHTML += row;
                });

                Params.set('status', filterStatus)
                search_key = document.getElementById('category-search').value
                if (search_key){
                    Params.set('search', search_key)
                }
                var filter = ''
                if (!window.location.pathname.includes('/filter')) {
                    filter = 'filter'
                }
                const newUrl = `${window.location.pathname}${filter}?${Params.toString()}`;
                history.pushState(null, '', newUrl);
            })
            .catch(error => console.error('Error:', error));
    }
});


// Live search
let timeout = null;

function debounce(func, delay) {
    return function () {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(this, arguments);
        }, delay);
    };
}

if (elSearch){
    elSearch.addEventListener('input', debounce(function (event) {
        const query = event.target.value;
        const params = new URLSearchParams(window.location.search);

        let newUrl =  window.location.pathname;
        if (query) {
            params.set('search', query);
        } else {
            params.delete('search');
        }
        newUrl += `?${params.toString()}`;
        window.location.href = newUrl;
    }, 300));
}


// Clear search
if (elClearSearch){
    elClearSearch.addEventListener('click', function () {
        document.getElementById('category-search').value = '';
        const params = new URLSearchParams(window.location.search);
        let FLAG_EMPTY = false
        if ([...params].length === 1 && params.get('search')){
            FLAG_EMPTY = true
        }
        params.delete('search');
        var newURL = `${window.location.pathname}?${params.toString()}`;
        if (FLAG_EMPTY){
            newURL = newURL.replace('filter?', '');
        }
        window.history.replaceState({}, '', newURL);

        window.location.href = newURL;
    });
}



// Pagination
function navigateToPage(pageNumber) {
    const urlParams = new URLSearchParams(window.location.search);

    urlParams.set('page', pageNumber);

    window.location.href = `?${urlParams.toString()}`;
}

// Ngày giờ hiện tại
function setCurrentDateTime() {
        const now = new Date();
        const date = now.toISOString().slice(0, 10); // Lấy ngày ở định dạng YYYY-MM-DD
        const time = now.toTimeString().slice(0, 5); // Lấy giờ ở định dạng HH:MM

        document.getElementById('publish_date').value = date;
        document.getElementById('publish_date_time').value = time;
    }

// Tagify
document.addEventListener('DOMContentLoaded', function() {
    var input = document.querySelector('#tags');
    if (input) {
        var tagify = new Tagify(input, {
            whitelist: [],
            maxTags: 10,
            dropdown: {
                maxItems: 20,
                classname: 'tags-look',
                enabled: 0,
                closeOnSelect: false
            }
        });
        fetch('/myadmin/get-tags/') 
        .then(response => response.json())
        .then(data => {
            tagify.settings.whitelist = data;  
        })
        .catch(error => console.error('Error fetching tags:', error));
    }
    
});

if (elImageInput){
    elImageInput.addEventListener("change", function(event) {
        var file = event.target.files[0];
    
       if (file) {
        // Ẩn ảnh cũ nếu có
        if (elOldImagePreview) {
            console.log('ANH CUUUUU')
            elOldImagePreview.style.display = "none";
        }

        // Hiển thị ảnh mới
        var reader = new FileReader();
        reader.onload = function(e) {
            elNewImagePreview.src = e.target.result;
            elNewImagePreview.style.display = "block";  // Hiển thị ảnh mới
        }
        reader.readAsDataURL(file);
    } else {
        // Hiển thị lại ảnh cũ nếu không có ảnh mới
        if (elOldImagePreview) {
            elOldImagePreview.style.display = "block";
        }
        elNewImagePreview.src = "#";
        elNewImagePreview.style.display = "none";  // Ẩn ảnh mới nếu không có ảnh nào được chọn
    }
    });
}



