# Job Board PostgreSQL Database Design

## Entity Relationship Diagram

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     User        │    │    Company      │    │    Category     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │    │ id (PK)         │    │ id (PK)         │
│ username        │    │ name            │    │ name            │
│ email           │    │ description     │    │ slug            │
│ password        │    │ website         │    │ description     │
│ first_name      │    │ logo_url        │    │ is_active       │
│ last_name       │    │ location        │    │ created_at      │
│ role            │    │ size            │    │ updated_at      │
│ phone           │    │ founded_year    │    └─────────────────┘
│ bio             │    │ industry        │              │
│ profile_pic     │    │ is_verified     │              │
│ location        │    │ created_at      │              │
│ resume_url      │    │ updated_at      │              │
│ is_active       │    └─────────────────┘              │
│ date_joined     │              │                       │
│ last_login      │              │                       │
└─────────────────┘              │                       │
         │                       │                       │
         │                       │                       │
         │    ┌─────────────────┐│                       │
         │    │      Job        ││                       │
         │    ├─────────────────┤│                       │
         │    │ id (PK)         ││                       │
         │    │ title           ││                       │
         │    │ description     ││                       │
         │    │ requirements    ││                       │
         │    │ location        ││                       │
         │    │ job_type        ││                       │
         │    │ experience_level││                       │
         │    │ salary_min      ││                       │
         │    │ salary_max      ││                       │
         │    │ currency        ││                       │
         │    │ is_remote       ││                       │
         │    │ is_active       ││                       │
         │    │ featured        ││                       │
         │    │ application_url ││                       │
         │    │ expires_at      ││                       │
         │    │ created_at      ││                       │
         │    │ updated_at      ││                       │
         │    │ company_id (FK) │┘                       │
         │    │ category_id (FK)│←───────────────────────┘
         │    │ posted_by (FK)  │←───────────────────────┐
         │    └─────────────────┘                        │
         │              │                                │
         │              │                                │
         │              │                                │
         │    ┌─────────────────┐                        │
         └────→   Application   │                        │
              ├─────────────────┤                        │
              │ id (PK)         │                        │
              │ job_id (FK)     │←───────────────────────┘
              │ applicant_id(FK)│
              │ cover_letter    │
              │ resume_url      │
              │ status          │
              │ applied_at      │
              │ updated_at      │
              └─────────────────┘
```

## Database Tables Design

### 1. Users Table (Custom User Model)

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    role VARCHAR(20) DEFAULT 'user' CHECK (role IN ('admin', 'user', 'employer')),
    phone VARCHAR(20),
    bio TEXT,
    profile_pic VARCHAR(500),
    location VARCHAR(255),
    resume_url VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    date_joined TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Indexes for Users
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_is_active ON users(is_active);
```

### 2. Companies Table

```sql
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    website VARCHAR(500),
    logo_url VARCHAR(500),
    location VARCHAR(255),
    size VARCHAR(50) CHECK (size IN ('1-10', '11-50', '51-200', '201-500', '501-1000', '1000+')),
    founded_year INTEGER CHECK (founded_year >= 1800 AND founded_year <= EXTRACT(YEAR FROM NOW())),
    industry VARCHAR(100),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE INDEX idx_companies_name ON companies(name);
CREATE INDEX idx_companies_location ON companies(location);
CREATE INDEX idx_companies_industry ON companies(industry);
CREATE INDEX idx_companies_is_verified ON companies(is_verified);
```

### 3. Categories Table

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_is_active ON categories(is_active);
```

### 4. Jobs Table

```sql
CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    requirements TEXT,
    location VARCHAR(255),
    job_type VARCHAR(50) DEFAULT 'full_time' CHECK (job_type IN ('full_time', 'part_time', 'contract', 'freelance', 'internship')),
    experience_level VARCHAR(50) DEFAULT 'mid_level' CHECK (experience_level IN ('entry_level', 'mid_level', 'senior_level', 'executive')),
    salary_min DECIMAL(12, 2),
    salary_max DECIMAL(12, 2),
    currency VARCHAR(3) DEFAULT 'USD',
    is_remote BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    featured BOOLEAN DEFAULT FALSE,
    application_url VARCHAR(500),
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    company_id INTEGER REFERENCES companies(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    posted_by INTEGER REFERENCES users(id) ON DELETE SET NULL
);


CREATE INDEX idx_jobs_title ON jobs USING GIN (to_tsvector('english', title));
CREATE INDEX idx_jobs_description ON jobs USING GIN (to_tsvector('english', description));
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_job_type ON jobs(job_type);
CREATE INDEX idx_jobs_experience_level ON jobs(experience_level);
CREATE INDEX idx_jobs_is_active ON jobs(is_active);
CREATE INDEX idx_jobs_is_remote ON jobs(is_remote);
CREATE INDEX idx_jobs_featured ON jobs(featured);
CREATE INDEX idx_jobs_created_at ON jobs(created_at DESC);
CREATE INDEX idx_jobs_expires_at ON jobs(expires_at);
CREATE INDEX idx_jobs_company_id ON jobs(company_id);
CREATE INDEX idx_jobs_category_id ON jobs(category_id);
CREATE INDEX idx_jobs_salary_range ON jobs(salary_min, salary_max);


CREATE INDEX idx_jobs_active_location ON jobs(is_active, location) WHERE is_active = TRUE;
CREATE INDEX idx_jobs_active_category ON jobs(is_active, category_id) WHERE is_active = TRUE;
CREATE INDEX idx_jobs_active_experience ON jobs(is_active, experience_level) WHERE is_active = TRUE;
```

### 5. Applications Table

```sql
CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    applicant_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    cover_letter TEXT,
    resume_url VARCHAR(500),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'shortlisted', 'interviewed', 'rejected', 'accepted')),
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(job_id, applicant_id)
);


CREATE INDEX idx_applications_job_id ON applications(job_id);
CREATE INDEX idx_applications_applicant_id ON applications(applicant_id);
CREATE INDEX idx_applications_status ON applications(status);
CREATE INDEX idx_applications_applied_at ON applications(applied_at DESC);
```