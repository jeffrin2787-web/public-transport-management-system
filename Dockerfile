# ==============================================================================
# MULTI-STAGE DOCKERFILE FOR 24/7 PRODUCTION CLOUD HOSTING
# PROJECT: Public Transport Management and Passenger Travel Analysis System
# AUTHOR: Jeffrin (Reg No: 732925ITR040) | VCET Erode - 12
# ==============================================================================

# STAGE 1: Build Application with Maven and JDK 17
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app

# Copy pom.xml and download dependencies (layer caching)
COPY pom.xml .
RUN mvn dependency:go-offline -B

# Copy full source tree and compile/package
COPY src ./src
RUN mvn clean package -DskipTests

# STAGE 2: Lightweight Production Runtime Image
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app

# Non-root security user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Copy executable jar from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Expose HTTP port (Render uses environment variable PORT, default 8080)
EXPOSE 8080
ENV PORT=8080

# Run Spring Boot Application
ENTRYPOINT ["java", "-Djava.security.egd=file:/dev/./urandom", "-jar", "app.jar"]
