let passwordsTableVisible = true;

function togglePasswords() {
    const passwordsTable = document.getElementById('passwords-table');
    const toggleButton = document.getElementById('toggle-button');

    if (passwordsTableVisible) {
        passwordsTable.style.display = 'none';
        toggleButton.textContent = 'Show Passwords';
    } else {
        passwordsTable.style.display = 'table';
        toggleButton.textContent = 'Hide Passwords';
    }

    passwordsTableVisible = !passwordsTableVisible;
}

// Вызываем togglePasswords() для начального скрытия таблицы паролей
togglePasswords();
