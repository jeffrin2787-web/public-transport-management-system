package com.vcet.transport.model;

/**
 * Enumeration representing categories of buses in the public transit fleet.
 * Meets Unit 1 & 2 of 25ITT32 Java Programming.
 */
public enum BusType {
    AC_SLEEPER("AC Sleeper (2+1)"),
    SEMI_SLEEPER("Air Conditioned Semi-Sleeper (2+2)"),
    ULTRA_DELUXE("Ultra Deluxe Express"),
    NON_AC_SEATER("Standard Non-AC Seater (3+2)");

    private final String displayName;

    BusType(String displayName) {
        this.displayName = displayName;
    }

    public String getDisplayName() {
        return displayName;
    }
}
