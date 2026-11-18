# ==============================================================================
# MULTI-STAGE DOCKERFILE FOR 24/7 PRODUCTION CLOUD HOSTING
# PROJECT: Public Transport Management and Passenger Travel Analysis System
# AUTHOR: Jeffrin (Reg No: 732925ITR040) | VCET Erode - 12
# ==============================================================================

# STAGE 1: Build Application with Maven and JDK 17
FROM maven:3.9-eclipse-temurin-17 AS builder
WORKDIR /app

# Copy pom.xml and full source tree
COPY pom.xml .
COPY src ./src

# Build production executable JAR (skipping tests for speed)
RUN mvn clean package -DskipTests

# STAGE 2: Lightweight Production Runtime Image (Java 17 JRE)
FROM eclipse-temurin:17-jre-jammy
WORKDIR /app

# Non-root security user
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Copy executable jar from builder stage
COPY --from=builder /app/target/*.jar app.jar

# Render binds to environment variable PORT (default 8080 or 10000)
EXPOSE 8080
ENV PORT=8080

# Run Spring Boot Application with memory tuning for Render Free Tier (512MB)
ENTRYPOINT ["java", "-Xmx350m", "-XX:+UseContainerSupport", "-Dserver.port=${PORT}", "-Djava.security.egd=file:/dev/./urandom", "-jar", "app.jar"]
